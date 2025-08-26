package org.example

import org.eclipse.jetty.server.Server
import org.eclipse.jetty.servlet.ServletContextHandler
import org.eclipse.jetty.websocket.server.WebSocketHandler
import org.eclipse.jetty.websocket.servlet.WebSocketServletFactory
import org.eclipse.jetty.websocket.api.Session
import org.eclipse.jetty.websocket.api.annotations.OnWebSocketConnect
import org.eclipse.jetty.websocket.api.annotations.OnWebSocketClose
import org.eclipse.jetty.websocket.api.annotations.OnWebSocketMessage
import org.eclipse.jetty.websocket.api.annotations.WebSocket

@WebSocket
class ChatSocket {
    static def sessions = Collections.synchronizedSet(new HashSet<Session>())

    @OnWebSocketConnect
    void onConnect(Session session) {
        sessions.add(session)
        session.remote.sendString("Welcome to simple chat server")
    }

    @OnWebSocketClose
    void onClose(Session session, int statusCode, String reason) {
        sessions.remove(session)
    }

    @OnWebSocketMessage
    void onMessage(Session session, String message) {
        println "Received: $message"
        synchronized(sessions) {
            sessions.each { s ->
                if (s.isOpen()) {
                    s.remote.sendString(message)
                }
            }
        }
    }
}

class App {
    static void main(String[] args) {
        def server = new Server(9001)

        def context = new ServletContextHandler(ServletContextHandler.SESSIONS)
        context.contextPath = "/"
        server.handler = context

        def wsHandler = new WebSocketHandler() {
            @Override
            void configure(WebSocketServletFactory factory) {
                factory.register(ChatSocket)
            }
        }
        context.handler = wsHandler

        println "Starting WebSocket chat server on ws://localhost:9001/ws"
        server.start()
        server.join()
    }
}

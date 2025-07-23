#include "LLMInference.h"
#include <memory>
#include <iostream>
extern "C" {
#include "llama.h"
}

// No-op logger for llama.cpp
void llama_no_log(enum ggml_log_level, const char *, void *) {}

int main(int argc, char* argv[]) {
    // Disable llama.cpp logging
    llama_log_set(llama_no_log, nullptr);

    std::string modelPath = "../models/DeepSeek-R1-Distill-Qwen-1.5B-Q8_0.gguf";
    float temperature = 1.0f;
    float minP = 0.05f;
    std::unique_ptr<LLMInference> llmInference = std::make_unique<LLMInference>();
    llmInference->loadModel(modelPath, minP, temperature);
    llmInference->addChatMessage("You are a helpful assistant", "system");
    llmInference->startCompletion("What is the capital of France?");
    std::string predictedToken;
    while ((predictedToken = llmInference->completionLoop()) != "[EOG]") {
        std::cout << predictedToken;
        fflush(stdout);
    }
    std::cout << '\n';
    return 0;
}
﻿using System;
using System.Collections.Generic;
using System.Linq;

namespace Kusto.Language.Binding
{
    using Symbols;

    /// <summary>
    /// Models nested scoping for let variables and function parameters.
    /// </summary>
    internal class LocalScope
    {
        private readonly LocalScope _outerScope;
        private Dictionary<string, Symbol> _symbols;
        private LocalScope _sharedSymbols;

        private LocalScope(Dictionary<string, Symbol> symbols, LocalScope outerScope, LocalScope sharedScope)
        {
            _symbols = symbols;
            _outerScope = GetMinimalOuterScope(outerScope);
            _sharedSymbols = sharedScope;
        }

        private static LocalScope GetMinimalOuterScope(LocalScope outerScope)
        {
            while (outerScope != null 
                && outerScope._symbols == null 
                && outerScope._sharedSymbols == null)
            {
                outerScope = outerScope._outerScope;
            }

            return outerScope;
        }

        /// <summary>
        /// Create a new instance of a <see cref="LocalScope"/>
        /// </summary>
        /// <param name="outerScope">An optional outer scope.</param>
        public LocalScope(LocalScope outerScope = null)
            : this(null, outerScope, null)
        {
        }

        /// <summary>
        /// Returns true if this scope has a matching symbol.
        /// </summary>
        public bool HasSymbol(string name)
        {
            return (_symbols != null && _symbols.ContainsKey(name))
                || (_sharedSymbols != null && _sharedSymbols.HasSymbol(name));
        }

        /// <summary>
        /// Returns true if this scope has a matching symbol.
        /// </summary>
        public bool HasSymbol(string name, SymbolMatch match)
        {
            return (_symbols != null && _symbols.TryGetValue(name, out var symbol) && symbol.Matches(match))
                || (_sharedSymbols != null && _sharedSymbols.HasSymbol(name, match));
        }

        /// <summary>
        /// Returns true if this scope has a matching symbol.
        /// </summary>
        public bool HasSymbol(SymbolMatch match)
        {
            return (_symbols != null && _symbols.Values.Any(s => s.Matches(match)))
                || (_sharedSymbols != null && _sharedSymbols.HasSymbol(match));
        }

        /// <summary>
        /// Returns true if this scope or any outer scope has a matching symbol.
        /// </summary>
        public bool ContainsSymbol(string name)
        {
            var scope = this;
            while (scope != null)
            {
                if (scope.HasSymbol(name))
                    return true;
                scope = scope._outerScope;
            }

            return false;
        }

        /// <summary>
        /// Returns true if this scope or any outer scope has a matching symbol.
        /// </summary>
        public bool ContainsSymbol(string name, SymbolMatch match)
        {
            var scope = this;
            while (scope != null)
            {
                if (scope.HasSymbol(name, match))
                    return true;
                scope = scope._outerScope;
            }

            return false;
        }

        /// <summary>
        /// Returns true if this scope or any outer scope has a matching symbol.
        /// </summary>
        public bool ContainsSymbol(SymbolMatch match)
        {
            var scope = this;
            while (scope != null)
            {
                if (scope.HasSymbol(match))
                    return true;
                scope = scope._outerScope;
            }

            return false;
        }

        /// <summary>
        /// Makes a copy of this <see cref="LocalScope"/>.
        /// </summary>
        public LocalScope Copy()
        {
            // if we have any non-shared symbols, then move them into shared chain of symbols that
            // can be shared w/o fear of modification (basically copy-on-fear-of-writing).
            if (_symbols != null && _symbols.Count > 0)
            {
                _sharedSymbols = new LocalScope(_symbols, null, _sharedSymbols);
                _symbols = null;
            }

            return new LocalScope(null, _outerScope, _sharedSymbols);
        }

        /// <summary>
        /// Add a <see cref="Symbol"/> to the <see cref="LocalScope"/>
        /// </summary>
        public bool AddSymbol(Symbol symbol)
        {
            if (symbol != null)
            {
                if (_symbols == null)
                {
                    _symbols = new Dictionary<string, Symbol>();
                }

                _symbols[symbol.Name] = symbol;

                if (!string.IsNullOrEmpty(symbol.AlternateName))
                {
                    _symbols[symbol.AlternateName] = symbol;
                }

                return true;
            }

            return false;
        }

        /// <summary>
        /// Adds a collection of <see cref="Symbol"/> to the <see cref="LocalScope"/>.
        /// </summary>
        public void AddSymbols(IEnumerable<Symbol> symbols)
        {
            foreach (var symbol in symbols)
            {
                AddSymbol(symbol);
            }
        }

        /// <summary>
        /// Gets all the matching symbols in this scope and then any outer scopes.
        /// If any named matches are found in this scope, all other named matches from outer scopes are ignored.
        /// </summary>
        public void GetSymbols(string name, SymbolMatch match, List<Symbol> symbols)
        {
            var originalCount = symbols.Count;

            if (_symbols != null)
            {
                if (name != null)
                {
                    if (_symbols.TryGetValue(name, out var decl) && decl.Matches(name, match))
                    {
                        symbols.Add(decl);
                    }
                }
                else
                {
                    foreach (var symbol in _symbols.Values)
                    {
                        if (symbol.Matches(match))
                        {
                            symbols.Add(symbol);
                        }
                    }
                }
            }

            if (_sharedSymbols != null
                && (name == null || symbols.Count == originalCount))
            {
                _sharedSymbols.GetSymbols(name, match, symbols);
            }

            if (_outerScope != null
                && (name == null || symbols.Count == originalCount))
            {
                _outerScope.GetSymbols(name, match, symbols);
            }
        }

        /// <summary>
        /// Gets all the matching symbols in this scope and then any outer scopes.
        /// If any named matches are found in this scope, all other named matches from outer scopes are ignored.
        /// </summary>
        public void GetSymbols(string name, List<Symbol> symbols)
        {
            GetSymbols(name, SymbolMatch.Any, symbols);
        }

        /// <summary>
        /// Gets all the matching symbols in the scope, and then from any outer scopes.
        /// If any named matches are found in this scope, all other named matches from outer scopes are ignored.
        /// </summary>
        public void GetSymbols(SymbolMatch match, List<Symbol> symbols)
        {
            GetSymbols(null, match, symbols);
        }
    }
}
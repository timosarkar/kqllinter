﻿using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace Kusto.Language.Syntax
{
    using Utils;

    /// <summary>
    /// A list of <see cref="SyntaxElement"/>'s.
    /// </summary>
    public abstract class SyntaxList : SyntaxNode //, IReadOnlyList<SyntaxElement>
    {
        private readonly SyntaxElement[] elements;

        protected SyntaxList(SyntaxElement[] elements, IReadOnlyList<Diagnostic> diagnostics)
            : base(diagnostics)
        {
            this.elements = elements;

            for (int i = 0; i < elements.Length; i++)
            {
                this.elements[i] = Attach(elements[i]);
            }

            this.Init();
        }

        public override SyntaxKind Kind => SyntaxKind.List;

        public virtual Type ElementType => null;

        /// <summary>
        /// Gets the element at the index.
        /// </summary>
        public SyntaxElement this[int index] => elements[index];

        /// <summary>
        /// The number of elements in the list.
        /// </summary>
        public int Count => elements.Length;

        public IEnumerator<SyntaxElement> GetEnumerator()
        {
            return ((IEnumerable<SyntaxElement>)this.elements).GetEnumerator();
        }

        /// <summary>
        /// The number of child elements this element has.
        /// </summary>
        public override int ChildCount => this.Count;

        /// <summary>
        /// Get the child of this element at the specified index.
        /// </summary>
        public override SyntaxElement GetChild(int index) => this.elements[index];

        protected IReadOnlyList<SyntaxElement> GetElements()
        {
            return this.elements;
        }

        public override void Accept(SyntaxVisitor visitor)
        {
            visitor.VisitList(this);
        }

        public override TResult Accept<TResult>(SyntaxVisitor<TResult> visitor)
        {
            return visitor.VisitList(this);
        }
    }

    /// <summary>
    /// A list of <see cref="SyntaxElement"/>'s.
    /// </summary>
    public sealed class SyntaxList<TElement> : SyntaxList, IReadOnlyList<TElement>
        where TElement : SyntaxElement
    {
        public SyntaxList(IEnumerable<TElement> elements, IReadOnlyList<Diagnostic> diagnostics = null)
            : base(elements.ToArray(), diagnostics)
        {
        }

        public SyntaxList(params TElement[] elements)
            : base(elements, null)
        {
        }

        public override SyntaxKind Kind => SyntaxKind.List;

        public override Type ElementType => typeof(TElement);

        private static TElement[] Copy(IReadOnlyList<TElement> list)
        {
            var newArray = new TElement[list.Count];

            for (int i = 0; i < newArray.Length; i++)
            {
                newArray[i] = list[i];
            }

            return newArray;
        }

        /// <summary>
        /// Gets the element at the index.
        /// </summary>
        public new TElement this[int index] => (TElement)base[index];

        public new IEnumerator<TElement> GetEnumerator()
        {
            return ((IEnumerable<TElement>)this.GetElements()).GetEnumerator();
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return this.GetEnumerator();
        }

        /// <summary>
        /// Creates a copy of this <see cref="SyntaxList{TElement}"/>
        /// </summary>
        public new SyntaxList<TElement> Clone(bool includeDiagnostics = true) => (SyntaxList<TElement>)this.CloneCore(includeDiagnostics);

        protected override SyntaxElement CloneCore(bool includeDiagnostics)
        {
            var oldElements = this.GetElements();
            var newElements = new TElement[oldElements.Count];

            for (int i = 0; i < newElements.Length; i++)
            {
                newElements[i] = (TElement)oldElements[i].Clone(includeDiagnostics);
            }

            return new SyntaxList<TElement>(newElements);
        }

        public static SyntaxList<TElement> Empty() => new SyntaxList<TElement>(new TElement[0]);
    }
}
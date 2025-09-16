﻿using System;
using System.Collections.Generic;

namespace Kusto.Language.Editor
{
    using Utils;

    /// <summary>
    /// The elements in the code that are related to the element at a particular cursor position.
    /// </summary>
    public class RelatedInfo
    {
        public IReadOnlyList<RelatedElement> Elements { get; }

        public int CurrentIndex { get; }

        public RelatedInfo(IReadOnlyList<RelatedElement> elements, int currentIndex)
        {
            this.Elements = elements;
            this.CurrentIndex = currentIndex;
        }

        public int GetNextIndex(int index)
        {
            if (index < this.Elements.Count - 1)
            {
                return index + 1;
            }
            else
            {
                return 0;
            }
        }

        public int GetPreviousIndex(int index)
        {
            if (index > 0)
            {
                return index - 1;
            }
            else
            {
                return this.Elements.Count - 1;
            }
        }

        public static readonly RelatedInfo Empty = new RelatedInfo(EmptyReadOnlyList<RelatedElement>.Instance, 0);
    }

    public enum RelatedElementKind
    {
        /// <summary>
        /// The element is a piece of syntax that is related to the other elements structurally.
        /// </summary>
        Syntax,

        /// <summary>
        /// The element is a named reference to a common item
        /// </summary>
        Reference,

        /// <summary>
        /// The element is a named declaration of a common item
        /// </summary>
        Declaration,

        /// <summary>
        /// The element is related to other elements, but does not name a common item.
        /// </summary>
        Other
    }

    /// <summary>
    /// An element of the text that is related in some way to another element.
    /// </summary>
    public class RelatedElement
    {
        /// <summary>
        /// The text range of the <see cref="RelatedElement"/>
        /// </summary>
        public TextRange Range { get; }

        /// <summary>
        /// The starting text position of the <see cref="RelatedElement"/>
        /// </summary>
        public int Start => Range.Start;

        /// <summary>
        /// The text length of the <see cref="RelatedElement"/>
        /// </summary>
        public int Length => Range.Length;

        /// <summary>
        /// The text position after the end of the <see cref="RelatedElement"/>
        /// </summary>
        public int End => this.Range.End;

        /// <summary>
        /// The kind of related element.
        /// </summary>
        public RelatedElementKind Kind { get; }

        /// <summary>
        /// The placement of the cursor when moving to the left,
        /// </summary>
        public int CursorLeft { get; }

        /// <summary>
        /// The placement of the cursor when moving to the right.
        /// </summary>
        public int CursorRight { get; }

        public RelatedElement(TextRange range, RelatedElementKind kind, int cursorLeft, int cursorRight)
        {
            this.Range = range;
            this.Kind = kind;
            this.CursorLeft = cursorLeft;
            this.CursorRight = cursorRight;
        }

        public RelatedElement(TextRange range, RelatedElementKind kind)
            : this(range, kind, range.Start, range.End)
        {
        }

        public RelatedElement(int start, int length, RelatedElementKind kind, int cursorLeft, int cursorRight)
            : this(new TextRange(start, length), kind, cursorLeft, cursorRight) 
        { 
        }

        public RelatedElement(int start, int length, RelatedElementKind kind)
            : this(new TextRange(start, length), kind, start, start + length)
        {
        }
    }
}
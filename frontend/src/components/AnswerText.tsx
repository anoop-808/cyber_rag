import React from 'react';

/**
 * Lightweight, dependency-free renderer for LLM answer text.
 * Supports headings, bullet/numbered lists, inline code, fenced
 * code blocks, blockquotes, bold, italics, and links — rendering
 * the raw backend answer without modifying its content.
 */

interface InlineToken {
    type: 'text' | 'code' | 'bold' | 'italic' | 'link';
    value: string;
    href?: string;
}

const INLINE_PATTERN = /(`[^`]+`)|(\*\*[^*]+\*\*)|(\*[^*]+\*)|(\[[^\]]+\]\([^)\s]+\))/g;

function tokenizeInline(text: string): InlineToken[] {
    const tokens: InlineToken[] = [];
    let lastIndex = 0;
    let match: RegExpExecArray | null;

    while ((match = INLINE_PATTERN.exec(text)) !== null) {
        if (match.index > lastIndex) {
            tokens.push({ type: 'text', value: text.slice(lastIndex, match.index) });
        }
        const token = match[0];
        if (token.startsWith('`')) {
            tokens.push({ type: 'code', value: token.slice(1, -1) });
        } else if (token.startsWith('**')) {
            tokens.push({ type: 'bold', value: token.slice(2, -2) });
        } else if (token.startsWith('*')) {
            tokens.push({ type: 'italic', value: token.slice(1, -1) });
        } else {
            const link = /^\[([^\]]+)\]\(([^)\s]+)\)$/.exec(token);
            if (link) {
                tokens.push({ type: 'link', value: link[1], href: link[2] });
            } else {
                tokens.push({ type: 'text', value: token });
            }
        }
        lastIndex = match.index + token.length;
    }

    if (lastIndex < text.length) {
        tokens.push({ type: 'text', value: text.slice(lastIndex) });
    }
    return tokens;
}

function renderInline(text: string, keyBase: string): React.ReactNode {
    return tokenizeInline(text).map((token, i) => {
        const key = `${keyBase}-${i}`;
        switch (token.type) {
            case 'code':
                return <code key={key}>{token.value}</code>;
            case 'bold':
                return <strong key={key}>{token.value}</strong>;
            case 'italic':
                return <em key={key}>{token.value}</em>;
            case 'link':
                return (
                    <a key={key} href={token.href} target="_blank" rel="noopener noreferrer">
                        {token.value}
                    </a>
                );
            default:
                return token.value;
        }
    });
}

const isBlockStart = (line: string): boolean =>
    /^\s*(#{1,6}\s|```|~~~|>)/.test(line) || /^\s*([-*+]|\d+[.)])\s+/.test(line);

function parseBlocks(text: string): React.ReactNode[] {
    const lines = text.split('\n');
    const blocks: React.ReactNode[] = [];
    let i = 0;
    let key = 0;

    while (i < lines.length) {
        const line = lines[i];

        // Fenced code block
        if (/^\s*```/.test(line) || /^\s*~~~/.test(line)) {
            const buf: string[] = [];
            i += 1;
            while (i < lines.length && !/^\s*(```|~~~)/.test(lines[i])) {
                buf.push(lines[i]);
                i += 1;
            }
            i += 1; // Skip closing fence (or EOF)
            blocks.push(
                <pre key={key++}>
                    <code>{buf.join('\n')}</code>
                </pre>
            );
            continue;
        }

        // Heading
        const heading = /^#{1,6}\s+(.*)$/.exec(line.trim());
        if (heading) {
            const level = line.trim().match(/^#+/)?.[0].length ?? 2;
            const Tag = (level <= 2 ? 'h2' : level === 3 ? 'h3' : 'h4') as 'h2' | 'h3' | 'h4';
            blocks.push(<Tag key={key++}>{renderInline(heading[1], `h${key}`)}</Tag>);
            i += 1;
            continue;
        }

        // Blockquote
        if (/^\s*>/.test(line)) {
            const buf: string[] = [];
            while (i < lines.length && /^\s*>/.test(lines[i])) {
                buf.push(lines[i].replace(/^\s*>\s?/, ''));
                i += 1;
            }
            blocks.push(<blockquote key={key++}>{parseBlocks(buf.join('\n'))}</blockquote>);
            continue;
        }

        // List
        if (/^\s*([-*+]|\d+[.)])\s+/.test(line)) {
            const items: { text: string; ordered: boolean }[] = [];
            while (i < lines.length) {
                const item = /^\s*([-*+]|\d+[.)])\s+(.*)$/.exec(lines[i]);
                if (!item) break;
                items.push({ text: item[2], ordered: /^\d+/.test(item[1]) });
                i += 1;
            }
            const ListTag = items[0]?.ordered ? 'ol' : 'ul';
            blocks.push(
                <ListTag key={key++}>
                    {items.map((item, idx) => (
                        <li key={idx}>{renderInline(item.text, `li${key}-${idx}`)}</li>
                    ))}
                </ListTag>
            );
            continue;
        }

        // Blank line
        if (!line.trim()) {
            i += 1;
            continue;
        }

        // Paragraph (collect until a blank line or a new block)
        const buf: string[] = [line.trim()];
        i += 1;
        while (i < lines.length && lines[i].trim() && !isBlockStart(lines[i])) {
            buf.push(lines[i].trim());
            i += 1;
        }
        blocks.push(<p key={key++}>{renderInline(buf.join(' '), `p${key}`)}</p>);
    }

    return blocks;
}

interface AnswerTextProps {
    text: string;
}

const AnswerText: React.FC<AnswerTextProps> = ({ text }) => {
    if (!text || !text.trim()) {
        return <p>No answer available.</p>;
    }
    return <>{parseBlocks(text)}</>;
};

export default AnswerText;

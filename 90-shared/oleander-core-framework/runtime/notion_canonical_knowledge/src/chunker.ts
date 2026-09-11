import { CHUNK_MAX_ESTIMATED_TOKENS, CHUNK_OVERLAP_ESTIMATED_TOKENS } from "./config";
import type { KnowledgeChunk } from "./types";

const CJK = /[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\u3040-\u30FF\uAC00-\uD7AF]/g;

export function estimateTokens(text: string): number {
  const cjk = text.match(CJK)?.length ?? 0;
  const remaining = Math.max(0, text.length - cjk);
  return cjk + Math.ceil(remaining / 4);
}

export function normalizeMarkdownForHash(markdown: string): string {
  return markdown
    .replace(/([?&])(X-Amz-(?:Algorithm|Credential|Date|Expires|SignedHeaders|Signature|Security-Token))=[^&#)\s]+/gi, "$1")
    .replace(/[?&]+(?=[)#\s]|$)/g, "")
    .replace(/[ \t]+$/gm, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

interface Section {
  path: string[];
  body: string;
}

function sections(markdown: string): Section[] {
  const lines = markdown.split(/\r?\n/);
  const headingStack: string[] = [];
  const out: Section[] = [];
  let body: string[] = [];
  let currentPath: string[] = [];

  const flush = () => {
    const value = body.join("\n").trim();
    if (value) out.push({ path: [...currentPath], body: value });
    body = [];
  };

  let inFence = false;
  for (const line of lines) {
    if (/^\s*```/.test(line)) inFence = !inFence;
    const heading = !inFence ? /^(#{1,6})\s+(.+?)\s*$/.exec(line) : null;
    if (heading) {
      flush();
      const depth = heading[1]?.length ?? 1;
      headingStack.length = depth - 1;
      headingStack[depth - 1] = heading[2] ?? "";
      currentPath = headingStack.filter(Boolean);
      continue;
    }
    body.push(line);
  }
  flush();
  if (out.length === 0 && markdown.trim()) out.push({ path: [], body: markdown.trim() });
  return out;
}

function hardSplit(text: string, maxTokens: number): string[] {
  if (estimateTokens(text) <= maxTokens) return [text];
  const sentences = text.split(/(?<=[。！？.!?；;])\s*/u).filter(Boolean);
  const parts: string[] = [];
  let current = "";
  for (const sentence of sentences.length > 1 ? sentences : [...text]) {
    const candidate = current ? `${current}${sentences.length > 1 ? " " : ""}${sentence}` : sentence;
    if (estimateTokens(candidate) > maxTokens && current) {
      parts.push(current.trim());
      current = sentence;
    } else {
      current = candidate;
    }
  }
  if (current.trim()) parts.push(current.trim());
  return parts;
}

function tailForOverlap(text: string, targetTokens: number): string {
  if (estimateTokens(text) <= targetTokens) return text;
  const chars = [...text];
  let start = chars.length;
  while (start > 0 && estimateTokens(chars.slice(start - 1).join("")) <= targetTokens) start -= 1;
  return chars.slice(start).join("").trim();
}

export function chunkMarkdown(markdown: string): KnowledgeChunk[] {
  const normalized = normalizeMarkdownForHash(markdown);
  const result: KnowledgeChunk[] = [];
  let ordinal = 0;

  for (const section of sections(normalized)) {
    const paragraphs = section.body.split(/\n\s*\n/).filter((part) => part.trim());
    let current = "";
    let previousTail = "";

    const emit = () => {
      const text = current.trim();
      if (!text) return;
      result.push({
        ordinal: ordinal++,
        headingPath: section.path,
        text,
        tokenEstimate: estimateTokens(text),
      });
      previousTail = tailForOverlap(text, CHUNK_OVERLAP_ESTIMATED_TOKENS);
      current = "";
    };

    for (const paragraph of paragraphs) {
      for (const piece of hardSplit(paragraph.trim(), CHUNK_MAX_ESTIMATED_TOKENS)) {
        const prefix = current ? current : previousTail;
        const candidate = prefix ? `${prefix}\n\n${piece}` : piece;
        if (estimateTokens(candidate) > CHUNK_MAX_ESTIMATED_TOKENS && current) {
          emit();
          current = previousTail ? `${previousTail}\n\n${piece}` : piece;
          if (estimateTokens(current) > CHUNK_MAX_ESTIMATED_TOKENS) {
            current = piece;
            emit();
          }
        } else if (estimateTokens(candidate) > CHUNK_MAX_ESTIMATED_TOKENS) {
          current = piece;
          emit();
        } else {
          current = candidate;
        }
      }
    }
    emit();
  }
  return result;
}

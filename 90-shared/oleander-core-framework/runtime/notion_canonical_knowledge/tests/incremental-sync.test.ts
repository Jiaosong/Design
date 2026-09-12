import { describe, expect, it } from "vitest";

import { buildNotesDeltaQueryPayload } from "../src/notion";

describe("incremental Notion sweep", () => {
  it("builds a bounded last-edited-time query with stable ordering", () => {
    expect(buildNotesDeltaQueryPayload(
      "2026-09-12T10:00:00.000Z",
      "2026-09-12T10:10:00.000Z",
      "cursor-1",
    )).toEqual({
      page_size: 100,
      result_type: "page",
      filter: {
        and: [
          {
            timestamp: "last_edited_time",
            last_edited_time: { on_or_after: "2026-09-12T10:00:00.000Z" },
          },
          {
            timestamp: "last_edited_time",
            last_edited_time: { on_or_before: "2026-09-12T10:10:00.000Z" },
          },
        ],
      },
      sorts: [{ timestamp: "last_edited_time", direction: "ascending" }],
      start_cursor: "cursor-1",
    });
  });
});

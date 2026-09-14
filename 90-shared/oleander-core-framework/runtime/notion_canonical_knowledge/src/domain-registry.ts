import { DOMAIN_FIELDS } from "./config";
import { propertyText } from "./normalize";
import type { NotionPage } from "./types";

export interface DomainRegistrySurfaceRow {
  pageId: string;
  title: string | null;
  level: string | null;
  frameworkPath: string | null;
  governanceState: string | null;
  inTrash: boolean;
  lastEditedTime: string | null;
}

export function domainRegistrySurfaceRows(pages: NotionPage[]): DomainRegistrySurfaceRow[] {
  return pages.map((page) => ({
    pageId: page.id,
    title: propertyText(page.properties?.[DOMAIN_FIELDS.title]),
    level: propertyText(page.properties?.[DOMAIN_FIELDS.level]),
    frameworkPath: propertyText(page.properties?.[DOMAIN_FIELDS.frameworkPath]),
    governanceState: propertyText(page.properties?.[DOMAIN_FIELDS.governanceState]),
    inTrash: page.in_trash === true,
    lastEditedTime: page.last_edited_time ?? null,
  }));
}

export function activeL2DomainRows(rows: DomainRegistrySurfaceRow[]): DomainRegistrySurfaceRow[] {
  return rows
    .filter((row) => row.level?.startsWith("L2") && row.governanceState === "ACTIVE" && !row.inTrash)
    .sort((a, b) => (a.frameworkPath ?? a.title ?? a.pageId).localeCompare(b.frameworkPath ?? b.title ?? b.pageId));
}

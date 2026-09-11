import { FIELDS, VALID_ELIGIBILITY, VALID_EXPLICIT_SPACES } from "./config";
import type {
  ExplicitRetrievalSpace,
  NormalizedPage,
  NotionPage,
  NotionProperty,
  SearchEligibility,
} from "./types";

function richTextPlain(value: unknown): string {
  if (!Array.isArray(value)) return "";
  return value
    .map((item) => {
      if (!item || typeof item !== "object") return "";
      const record = item as Record<string, unknown>;
      if (typeof record.plain_text === "string") return record.plain_text;
      const text = record.text;
      if (text && typeof text === "object" && typeof (text as Record<string, unknown>).content === "string") {
        return (text as Record<string, unknown>).content as string;
      }
      return "";
    })
    .join("");
}

export function propertyText(property: NotionProperty | undefined): string | null {
  if (!property) return null;
  const type = property.type;
  if (type === "title") return richTextPlain(property.title) || null;
  if (type === "rich_text") return richTextPlain(property.rich_text) || null;
  if (type === "select") {
    const select = property.select as Record<string, unknown> | null | undefined;
    return select && typeof select.name === "string" ? select.name : null;
  }
  if (type === "status") {
    const status = property.status as Record<string, unknown> | null | undefined;
    return status && typeof status.name === "string" ? status.name : null;
  }
  if (type === "url") return typeof property.url === "string" ? property.url : null;
  return null;
}

export function propertyRelationIds(property: NotionProperty | undefined): string[] {
  if (!property || property.type !== "relation" || !Array.isArray(property.relation)) return [];
  return property.relation
    .map((item) => (item && typeof item === "object" ? (item as Record<string, unknown>).id : null))
    .filter((id): id is string => typeof id === "string");
}

function normalizedUuid(value: string | null | undefined): string | null {
  return value ? value.replaceAll("-", "").toLowerCase() : null;
}

export function pageParentDataSourceId(page: NotionPage): string | null {
  const parent = page.parent;
  if (!parent) return null;
  if (typeof parent.data_source_id === "string") return parent.data_source_id;
  if (parent.type === "data_source_id" && typeof parent.data_source_id === "string") return parent.data_source_id;
  return null;
}

export function belongsToDataSource(page: NotionPage, expectedDataSourceId: string): boolean {
  return normalizedUuid(pageParentDataSourceId(page)) === normalizedUuid(expectedDataSourceId);
}

export function normalizePage(page: NotionPage): NormalizedPage {
  const properties = page.properties ?? {};
  const explicitSpaceRaw = propertyText(properties[FIELDS.retrievalSpace]);
  const explicitSpace = explicitSpaceRaw && VALID_EXPLICIT_SPACES.has(explicitSpaceRaw)
    ? (explicitSpaceRaw as ExplicitRetrievalSpace)
    : null;
  const eligibilityRaw = propertyText(properties[FIELDS.searchEligibility]);
  const eligibility = eligibilityRaw && VALID_ELIGIBILITY.has(eligibilityRaw)
    ? (eligibilityRaw as SearchEligibility)
    : null;

  return {
    pageId: page.id,
    canonicalId: propertyText(properties[FIELDS.canonicalId]),
    title: propertyText(properties[FIELDS.title]) ?? "",
    url: page.url ?? null,
    lastEditedTime: page.last_edited_time ?? null,
    inTrash: page.in_trash === true,
    parentDataSourceId: pageParentDataSourceId(page),
    retrievalSpace: explicitSpace,
    searchEligibility: eligibility,
    trustState: propertyText(properties[FIELDS.trustState]),
    governanceState: propertyText(properties[FIELDS.governanceState]),
    relationState: propertyText(properties[FIELDS.relationState]),
    contentLevel: propertyText(properties[FIELDS.contentLevel]),
    knowledgeRole: propertyText(properties[FIELDS.knowledgeRole]),
    primaryDomainIds: propertyRelationIds(properties[FIELDS.primaryDomain]),
    relatedDomainIds: propertyRelationIds(properties[FIELDS.relatedDomains]),
    sourceRelationIds: propertyRelationIds(properties[FIELDS.sourceRelations]),
    methodRelationIds: propertyRelationIds(properties[FIELDS.methodRelations]),
    replacementIds: propertyRelationIds(properties[FIELDS.replacements]),
    replacedDocumentIds: propertyRelationIds(properties[FIELDS.replacedDocuments]),
  };
}

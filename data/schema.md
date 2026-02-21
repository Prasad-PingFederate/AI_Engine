# Dataset Schema

Each document should be a JSON object in `data/documents.jsonl` with fields:

- `id` (string, required): Stable unique identifier.
- `title` (string, required): Human readable title.
- `content` (string, required): Full searchable body.
- `source_type` (string, required): One of `bible`, `person`, `article`, `sermon`, `qa`.
- `author` (string, optional): Author or translator.
- `book` (string, optional): Bible book if applicable.
- `chapter` (integer, optional): Bible chapter.
- `verse` (string, optional): Verse or verse range.
- `tags` (array[string], optional): Topical tags.
- `url` (string, optional): Reference URL.
- `published_at` (string, optional): ISO-8601 datetime/date.

## Example

```json
{
  "id": "bible-john-3-16",
  "title": "John 3:16",
  "content": "For God so loved the world...",
  "source_type": "bible",
  "author": "ESV",
  "book": "John",
  "chapter": 3,
  "verse": "16",
  "tags": ["salvation", "love", "gospel"]
}
```

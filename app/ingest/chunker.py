from typing import List, Tuple
from app.config import settings
import re


# Simple sentence splitter — avoids heavy NLTK dependency
_SENT_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')




def split_into_sentences(text: str) -> List[str]:
# split on punctuation followed by whitespace
s = [s.strip() for s in _SENT_SPLIT_RE.split(text) if s.strip()]
return s




def token_len(text: str) -> int:
# approximate tokenizer using whitespace; for production use tiktoken or tokenizer matching your model
return len(text.split())




def chunk_text(text: str, target_tokens: int = None, overlap_tokens: int = None) -> List[Tuple[str, int, int]]:
target = target_tokens or settings.chunk_tokens
overlap = overlap_tokens or settings.chunk_overlap


sentences = split_into_sentences(text)
chunks = []
current = []
current_tokens = 0
offset = 0


for s in sentences:
s_tokens = token_len(s)
if current_tokens + s_tokens <= target:
current.append(s)
current_tokens += s_tokens
else:
chunk_text = " ".join(current).strip()
if chunk_text:
chunks.append((chunk_text, offset, offset + current_tokens))
offset += current_tokens - overlap
current = [s]
current_tokens = s_tokens


if current:
chunk_text_ = " ".join(current).strip()
chunks.append((chunk_text_, offset, offset + current_tokens))


return chunks
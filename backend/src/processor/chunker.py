"""
Content Chunker Module for Physical AI Book Content

This module handles splitting content into semantically coherent chunks for embedding.
"""
from typing import List, Dict
from ..utils.logger import app_logger
from ..utils.config import Config


class ContentChunker:
    """Class to split content into semantically coherent chunks for embedding."""

    def __init__(self, config: Config):
        self.config = config

    def chunk_content(self, content: str, metadata: Dict = None) -> List[Dict]:
        """
        Split content into chunks with overlapping context.

        Args:
            content: Text content to chunk
            metadata: Metadata associated with the content

        Returns:
            List of chunk dictionaries with text and metadata
        """
        if not content:
            return []

        # Split content into sentences or paragraphs as base units
        sentences = self._split_into_sentences(content)

        # Create chunks based on the configured size
        chunks = self._create_chunks(sentences, metadata)

        return chunks

    def _split_into_sentences(self, content: str) -> List[str]:
        """
        Split content into sentences while preserving paragraph structure.

        Args:
            content: Text content to split

        Returns:
            List of sentences or paragraph segments
        """
        # Split by common sentence endings first
        import re
        sentences = re.split(r'(?<=[.!?])\s+', content)

        # Clean up the sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                cleaned_sentences.append(sentence)

        return cleaned_sentences

    def _create_chunks(self, sentences: List[str], metadata: Dict) -> List[Dict]:
        """
        Create overlapping chunks from sentences.

        Args:
            sentences: List of sentences to chunk
            metadata: Metadata to include with each chunk

        Returns:
            List of chunk dictionaries
        """
        chunks = []
        current_chunk = ""
        current_length = 0
        sentence_idx = 0

        while sentence_idx < len(sentences):
            sentence = sentences[sentence_idx]
            sentence_length = len(sentence.split())

            # Check if adding this sentence would exceed the chunk size
            if current_length + sentence_length <= self.config.chunk_size or current_chunk == "":
                # Add sentence to current chunk
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
                current_length += sentence_length
                sentence_idx += 1
            else:
                # Create a chunk with the current content
                chunk_metadata = self._create_chunk_metadata(metadata, sentence_idx, len(sentences))
                chunks.append({
                    "text": current_chunk,
                    "metadata": chunk_metadata,
                    "chunk_id": f"chunk_{len(chunks)}"
                })

                # Start a new chunk with overlap if possible
                if self.config.chunk_overlap > 0 and sentence_idx > 0:
                    # Create overlap by going back and including some previous sentences
                    overlap_sentences = self._get_overlap_sentences(sentences, sentence_idx)
                    current_chunk = " ".join(overlap_sentences) + " " + sentence
                    current_length = len(current_chunk.split())
                    sentence_idx += 1
                else:
                    current_chunk = sentence
                    current_length = sentence_length
                    sentence_idx += 1

        # Add the final chunk if it has content
        if current_chunk:
            chunk_metadata = self._create_chunk_metadata(metadata, sentence_idx, len(sentences))
            chunks.append({
                "text": current_chunk,
                "metadata": chunk_metadata,
                "chunk_id": f"chunk_{len(chunks)}"
            })

        return chunks

    def _get_overlap_sentences(self, sentences: List[str], current_idx: int) -> List[str]:
        """
        Get sentences for overlap from previous content.

        Args:
            sentences: List of all sentences
            current_idx: Current sentence index

        Returns:
            List of sentences for overlap
        """
        overlap_sentences = []
        words_count = 0

        # Go backwards from the current index to get overlap
        for i in range(current_idx - 1, max(-1, current_idx - 5), -1):  # Look at most 5 sentences back
            sentence = sentences[i]
            sentence_words = len(sentence.split())

            if words_count + sentence_words <= self.config.chunk_overlap:
                overlap_sentences.insert(0, sentence)  # Insert at the beginning to maintain order
                words_count += sentence_words
            else:
                break

        return overlap_sentences

    def _create_chunk_metadata(self, original_metadata: Dict, position: int, total: int) -> Dict:
        """
        Create metadata for a specific chunk.

        Args:
            original_metadata: Original content metadata
            position: Current position in the content
            total: Total number of sentences/segments

        Returns:
            Metadata dictionary for the chunk
        """
        chunk_metadata = original_metadata.copy() if original_metadata else {}

        # Add chunk-specific metadata
        chunk_metadata.update({
            "chunk_position": position,
            "total_content_segments": total,
            "chunk_size_config": self.config.chunk_size,
            "chunk_overlap_config": self.config.chunk_overlap
        })

        return chunk_metadata
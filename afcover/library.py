"""
Reference Library for Afghan Cover Art Generator

Manages collections of reference artwork organized by artist and style.
Allows for storing, retrieving, and organizing reference images for
consistent style matching across multiple generations.
"""

import json
import os
import shutil
import zipfile
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple


class ReferenceLibrary:
    """
    Manages collections of reference artwork for Afghan cover art generation.
    
    Organizes references by:
    - Artist: Works by a specific musician/performer
    - Style: Collections representing a visual aesthetic
    
    Each collection stores:
    - Image files in a dedicated directory
    - Metadata in a JSON file (tags, notes, etc.)
    """
    
    def __init__(self, base_path: str = None):
        """
        Initialize the reference library.
        
        Args:
            base_path: Base directory for the reference library.
                      Defaults to ./references/ if not provided.
        """
        if base_path is None:
            # Default to the references directory within afcover
            self.base_path = Path(__file__).parent / "references"
        else:
            self.base_path = Path(base_path)
        
        # Ensure the base directories exist
        self.artists_path = self.base_path / "artists"
        self.styles_path = self.base_path / "styles"
        self.artists_path.mkdir(parents=True, exist_ok=True)
        self.styles_path.mkdir(parents=True, exist_ok=True)
    
    def list_collections(self, collection_type: str = "all") -> Dict[str, List[str]]:
        """
        List available reference collections.
        
        Args:
            collection_type: Type of collections to list ('artists', 'styles', or 'all')
        
        Returns:
            Dictionary with collections and their contents
        """
        result = {}
        
        if collection_type in ["artists", "all"]:
            artists = {}
            for artist_dir in self.artists_path.iterdir():
                if artist_dir.is_dir():
                    artist_name = artist_dir.name
                    artists[artist_name] = self._list_references_in_dir(artist_dir)
            result["artists"] = artists
        
        if collection_type in ["styles", "all"]:
            styles = {}
            for style_dir in self.styles_path.iterdir():
                if style_dir.is_dir():
                    style_name = style_dir.name
                    styles[style_name] = self._list_references_in_dir(style_dir)
            result["styles"] = styles
        
        return result
    
    def get_artist_references(self, artist_name: str) -> List[str]:
        """
        Get paths to reference images for a specific artist.
        
        Args:
            artist_name: Name of the artist
        
        Returns:
            List of paths to reference images
        """
        artist_dir = self.artists_path / artist_name
        if not artist_dir.exists():
            return []
        
        return self._list_references_in_dir(artist_dir)
    
    def get_style_references(self, style_name: str) -> List[str]:
        """
        Get paths to reference images for a specific style.
        
        Args:
            style_name: Name of the style
        
        Returns:
            List of paths to reference images
        """
        style_dir = self.styles_path / style_name
        if not style_dir.exists():
            return []
        
        return self._list_references_in_dir(style_dir)
    
    def add_artist_reference(
        self,
        artist_name: str,
        image_path: str,
        metadata: Dict[str, Any] = None,
        copy_file: bool = True,
    ) -> str:
        """
        Add a reference image to an artist collection.
        
        Args:
            artist_name: Name of the artist
            image_path: Path to the reference image
            metadata: Additional metadata for the image
            copy_file: If True, copy the file; if False, move it
        
        Returns:
            Path to the reference in the library
        """
        return self._add_reference(
            collection_type="artists",
            collection_name=artist_name,
            image_path=image_path,
            metadata=metadata,
            copy_file=copy_file,
        )
    
    def add_style_reference(
        self,
        style_name: str,
        image_path: str,
        metadata: Dict[str, Any] = None,
        copy_file: bool = True,
    ) -> str:
        """
        Add a reference image to a style collection.
        
        Args:
            style_name: Name of the style
            image_path: Path to the reference image
            metadata: Additional metadata for the image
            copy_file: If True, copy the file; if False, move it
        
        Returns:
            Path to the reference in the library
        """
        return self._add_reference(
            collection_type="styles",
            collection_name=style_name,
            image_path=image_path,
            metadata=metadata,
            copy_file=copy_file,
        )
    
    def remove_reference(self, reference_path: str) -> bool:
        """
        Remove a reference image from the library.
        
        Args:
            reference_path: Path to the reference image
        
        Returns:
            True if successful, False otherwise
        """
        path = Path(reference_path)
        
        # Check if the file exists and is within our library
        if not path.exists() or str(self.base_path) not in str(path.absolute()):
            return False
        
        # Remove the file
        path.unlink()
        
        # Update metadata
        collection_dir = path.parent
        metadata_path = collection_dir / "metadata.json"
        
        if metadata_path.exists():
            try:
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                
                # Remove this file's metadata if present
                if path.name in metadata.get("references", {}):
                    del metadata["references"][path.name]
                    
                    with open(metadata_path, "w") as f:
                        json.dump(metadata, f, indent=2)
            except Exception:
                pass
        
        return True
    
    def get_metadata(self, collection_type: str, collection_name: str) -> Dict[str, Any]:
        """
        Get metadata for a collection.
        
        Args:
            collection_type: Type of collection ('artists' or 'styles')
            collection_name: Name of the collection
        
        Returns:
            Dictionary with collection metadata
        """
        if collection_type == "artists":
            collection_dir = self.artists_path / collection_name
        elif collection_type == "styles":
            collection_dir = self.styles_path / collection_name
        else:
            raise ValueError(f"Unknown collection type: {collection_type}")
        
        metadata_path = collection_dir / "metadata.json"
        
        if metadata_path.exists():
            with open(metadata_path, "r") as f:
                return json.load(f)
        
        return {"name": collection_name, "references": {}}
    
    def update_metadata(
        self,
        collection_type: str,
        collection_name: str,
        metadata: Dict[str, Any],
    ) -> bool:
        """
        Update metadata for a collection.
        
        Args:
            collection_type: Type of collection ('artists' or 'styles')
            collection_name: Name of the collection
            metadata: New metadata
        
        Returns:
            True if successful, False otherwise
        """
        if collection_type == "artists":
            collection_dir = self.artists_path / collection_name
        elif collection_type == "styles":
            collection_dir = self.styles_path / collection_name
        else:
            raise ValueError(f"Unknown collection type: {collection_type}")
        
        # Ensure collection exists
        collection_dir.mkdir(parents=True, exist_ok=True)
        
        # Update the metadata file
        metadata_path = collection_dir / "metadata.json"
        
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        return True
    
    def _list_references_in_dir(self, directory: Path) -> List[str]:
        """List reference image paths in a directory."""
        image_extensions = [".jpg", ".jpeg", ".png", ".webp", ".gif"]
        references = []
        
        for file in directory.iterdir():
            if file.is_file() and file.suffix.lower() in image_extensions:
                references.append(str(file.absolute()))
        
        return references
    
    def batch_add_references(
        self,
        collection_type: str,
        collection_name: str,
        image_paths: List[str],
        metadata: Dict[str, Dict[str, Any]] = None,
        copy_files: bool = True,
    ) -> List[str]:
        """
        Add multiple reference images to a collection.
        
        Args:
            collection_type: Type of collection ('artists' or 'styles')
            collection_name: Name of the collection
            image_paths: List of paths to reference images
            metadata: Dictionary mapping image paths to their metadata
            copy_files: If True, copy the files; if False, move them
        
        Returns:
            List of paths to the references in the library
        """
        added_references = []
        metadata = metadata or {}
        
        for image_path in image_paths:
            try:
                image_metadata = metadata.get(image_path, {})
                ref_path = self._add_reference(
                    collection_type=collection_type,
                    collection_name=collection_name,
                    image_path=image_path,
                    metadata=image_metadata,
                    copy_file=copy_files,
                )
                added_references.append(ref_path)
            except Exception as e:
                print(f"Error adding reference {image_path}: {e}")
        
        return added_references
    
    def search_references(
        self,
        query: str,
        collection_type: str = "all",
        search_metadata: bool = True,
    ) -> Dict[str, List[str]]:
        """
        Search for references matching a query.
        
        Args:
            query: Search query
            collection_type: Type of collections to search ('artists', 'styles', or 'all')
            search_metadata: If True, also search in metadata fields
        
        Returns:
            Dictionary with matching references grouped by collection
        """
        results = {}
        collections = {}
        
        # Prepare search pattern
        pattern = re.compile(query, re.IGNORECASE)
        
        # Get collections to search
        if collection_type in ["artists", "all"]:
            for artist_dir in self.artists_path.iterdir():
                if artist_dir.is_dir():
                    collections[f"artists/{artist_dir.name}"] = artist_dir
        
        if collection_type in ["styles", "all"]:
            for style_dir in self.styles_path.iterdir():
                if style_dir.is_dir():
                    collections[f"styles/{style_dir.name}"] = style_dir
        
        # Search each collection
        for collection_key, collection_dir in collections.items():
            collection_results = []
            
            # Check filenames
            for file_path in collection_dir.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
                    if pattern.search(file_path.name):
                        collection_results.append(str(file_path.absolute()))
                        continue
            
            # Check metadata if requested
            if search_metadata:
                metadata_path = collection_dir / "metadata.json"
                if metadata_path.exists():
                    try:
                        with open(metadata_path, "r") as f:
                            metadata = json.load(f)
                        
                        # Check collection metadata
                        collection_text = json.dumps(
                            {k: v for k, v in metadata.items() if k != "references"}
                        )
                        if pattern.search(collection_text):
                            # Add all references if collection metadata matches
                            for file_path in collection_dir.iterdir():
                                if file_path.is_file() and file_path.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
                                    if str(file_path.absolute()) not in collection_results:
                                        collection_results.append(str(file_path.absolute()))
                            continue
                        
                        # Check individual reference metadata
                        if "references" in metadata:
                            for ref_name, ref_metadata in metadata["references"].items():
                                ref_path = collection_dir / ref_name
                                if ref_path.exists() and pattern.search(json.dumps(ref_metadata)):
                                    ref_abs_path = str(ref_path.absolute())
                                    if ref_abs_path not in collection_results:
                                        collection_results.append(ref_abs_path)
                    except Exception as e:
                        print(f"Error searching metadata in {collection_key}: {e}")
            
            if collection_results:
                results[collection_key] = collection_results
        
        return results
    
    def export_collection(
        self,
        collection_type: str,
        collection_name: str,
        output_path: str = None,
    ) -> str:
        """
        Export a collection as a zip file.
        
        Args:
            collection_type: Type of collection ('artists' or 'styles')
            collection_name: Name of the collection
            output_path: Path to save the zip file (defaults to collection_name.zip)
        
        Returns:
            Path to the exported zip file
        """
        # Determine the source directory
        if collection_type == "artists":
            collection_dir = self.artists_path / collection_name
        elif collection_type == "styles":
            collection_dir = self.styles_path / collection_name
        else:
            raise ValueError(f"Unknown collection type: {collection_type}")
        
        if not collection_dir.exists():
            raise FileNotFoundError(f"Collection not found: {collection_type}/{collection_name}")
        
        # Determine the output path
        if output_path is None:
            output_path = f"{collection_name}.zip"
        
        output_path = Path(output_path)
        
        # Create the zip file
        with zipfile.ZipFile(output_path, "w") as zip_file:
            for file_path in collection_dir.rglob("*"):
                if file_path.is_file():
                    zip_file.write(
                        file_path,
                        arcname=file_path.relative_to(collection_dir),
                    )
        
        return str(output_path.absolute())
    
    def import_collection(
        self,
        collection_type: str,
        collection_name: str,
        zip_path: str,
        overwrite: bool = False,
    ) -> Tuple[int, int]:
        """
        Import a collection from a zip file.
        
        Args:
            collection_type: Type of collection ('artists' or 'styles')
            collection_name: Name of the collection
            zip_path: Path to the zip file
            overwrite: If True, overwrite existing files
        
        Returns:
            Tuple of (number of files imported, number of files skipped)
        """
        # Determine the target directory
        if collection_type == "artists":
            collection_dir = self.artists_path / collection_name
        elif collection_type == "styles":
            collection_dir = self.styles_path / collection_name
        else:
            raise ValueError(f"Unknown collection type: {collection_type}")
        
        # Create the directory if it doesn't exist
        collection_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract the zip file
        imported = 0
        skipped = 0
        
        with zipfile.ZipFile(zip_path, "r") as zip_file:
            for file_info in zip_file.infolist():
                if not file_info.is_dir():
                    target_path = collection_dir / file_info.filename
                    
                    # Create parent directories if needed
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    if target_path.exists() and not overwrite:
                        skipped += 1
                        continue
                    
                    with zip_file.open(file_info) as source, open(target_path, "wb") as target:
                        shutil.copyfileobj(source, target)
                    
                    imported += 1
        
        return (imported, skipped)
    
    def _add_reference(
        self,
        collection_type: str,
        collection_name: str,
        image_path: str,
        metadata: Dict[str, Any] = None,
        copy_file: bool = True,
    ) -> str:
        """
        Add a reference image to a collection.
        
        Args:
            collection_type: Type of collection ('artists' or 'styles')
            collection_name: Name of the collection
            image_path: Path to the reference image
            metadata: Additional metadata for the image
            copy_file: If True, copy the file; if False, move it
        
        Returns:
            Path to the reference in the library
        """
        # Determine the target directory
        if collection_type == "artists":
            collection_dir = self.artists_path / collection_name
        elif collection_type == "styles":
            collection_dir = self.styles_path / collection_name
        else:
            raise ValueError(f"Unknown collection type: {collection_type}")
        
        # Create the directory if it doesn't exist
        collection_dir.mkdir(parents=True, exist_ok=True)
        
        # Prepare the image path
        source_path = Path(image_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Use the original filename or create a new one if needed
        target_path = collection_dir / source_path.name
        
        # If a file with the same name already exists, rename with a suffix
        if target_path.exists():
            base_name = source_path.stem
            extension = source_path.suffix
            counter = 1
            
            while target_path.exists():
                target_path = collection_dir / f"{base_name}_{counter}{extension}"
                counter += 1
        
        # Copy or move the file
        if copy_file:
            shutil.copy2(source_path, target_path)
        else:
            shutil.move(source_path, target_path)
        
        # Update metadata
        metadata_path = collection_dir / "metadata.json"
        collection_metadata = {}
        
        # Load existing metadata if available
        if metadata_path.exists():
            with open(metadata_path, "r") as f:
                collection_metadata = json.load(f)
        else:
            # Initialize with default structure
            collection_metadata = {
                "name": collection_name,
                "type": collection_type,
                "references": {}
            }
        
        # Ensure references dictionary exists
        if "references" not in collection_metadata:
            collection_metadata["references"] = {}
        
        # Add metadata for this reference
        reference_metadata = metadata or {}
        reference_metadata["file_name"] = target_path.name
        reference_metadata["added_at"] = Path(target_path).stat().st_mtime
        
        collection_metadata["references"][target_path.name] = reference_metadata
        
        # Save the updated metadata
        with open(metadata_path, "w") as f:
            json.dump(collection_metadata, f, indent=2)
        
        return str(target_path.absolute())


# Convenience functions to make the library easier to use

def list_references(collection_type: str = "all") -> Dict[str, List[str]]:
    """
    List available reference collections.
    
    Args:
        collection_type: Type of collections to list ('artists', 'styles', or 'all')
    
    Returns:
        Dictionary with collections
    """
    library = ReferenceLibrary()
    return library.list_collections(collection_type)


def get_artist_references(artist_name: str) -> List[str]:
    """
    Get paths to reference images for a specific artist.
    
    Args:
        artist_name: Name of the artist
    
    Returns:
        List of paths to reference images
    """
    library = ReferenceLibrary()
    return library.get_artist_references(artist_name)


def get_style_references(style_name: str) -> List[str]:
    """
    Get paths to reference images for a specific style.
    
    Args:
        style_name: Name of the style
    
    Returns:
        List of paths to reference images
    """
    library = ReferenceLibrary()
    return library.get_style_references(style_name)


def add_artist_reference(
    artist_name: str,
    image_path: str,
    metadata: Dict[str, Any] = None,
    copy_file: bool = True,
) -> str:
    """
    Add a reference image to an artist collection.
    
    Args:
        artist_name: Name of the artist
        image_path: Path to the reference image
        metadata: Additional metadata for the image
        copy_file: If True, copy the file; if False, move it
    
    Returns:
        Path to the reference in the library
    """
    library = ReferenceLibrary()
    return library.add_artist_reference(
        artist_name=artist_name,
        image_path=image_path,
        metadata=metadata,
        copy_file=copy_file,
    )


def add_style_reference(
    style_name: str,
    image_path: str,
    metadata: Dict[str, Any] = None,
    copy_file: bool = True,
) -> str:
    """
    Add a reference image to a style collection.
    
    Args:
        style_name: Name of the style
        image_path: Path to the reference image
        metadata: Additional metadata for the image
        copy_file: If True, copy the file; if False, move it
    
    Returns:
        Path to the reference in the library
    """
    library = ReferenceLibrary()
    return library.add_style_reference(
        style_name=style_name,
        image_path=image_path,
        metadata=metadata,
        copy_file=copy_file,
    )


def batch_add_artist_references(
    artist_name: str,
    image_paths: List[str],
    metadata: Dict[str, Dict[str, Any]] = None,
    copy_files: bool = True,
) -> List[str]:
    """
    Add multiple reference images to an artist collection.
    
    Args:
        artist_name: Name of the artist
        image_paths: List of paths to reference images
        metadata: Dictionary mapping image paths to their metadata
        copy_files: If True, copy the files; if False, move them
    
    Returns:
        List of paths to the references in the library
    """
    library = ReferenceLibrary()
    return library.batch_add_references(
        collection_type="artists",
        collection_name=artist_name,
        image_paths=image_paths,
        metadata=metadata,
        copy_files=copy_files,
    )


def batch_add_style_references(
    style_name: str,
    image_paths: List[str],
    metadata: Dict[str, Dict[str, Any]] = None,
    copy_files: bool = True,
) -> List[str]:
    """
    Add multiple reference images to a style collection.
    
    Args:
        style_name: Name of the style
        image_paths: List of paths to reference images
        metadata: Dictionary mapping image paths to their metadata
        copy_files: If True, copy the files; if False, move them
    
    Returns:
        List of paths to the references in the library
    """
    library = ReferenceLibrary()
    return library.batch_add_references(
        collection_type="styles",
        collection_name=style_name,
        image_paths=image_paths,
        metadata=metadata,
        copy_files=copy_files,
    )


def search_references(
    query: str,
    collection_type: str = "all",
    search_metadata: bool = True,
) -> Dict[str, List[str]]:
    """
    Search for references matching a query.
    
    Args:
        query: Search query
        collection_type: Type of collections to search ('artists', 'styles', or 'all')
        search_metadata: If True, also search in metadata fields
    
    Returns:
        Dictionary with matching references grouped by collection
    """
    library = ReferenceLibrary()
    return library.search_references(
        query=query,
        collection_type=collection_type,
        search_metadata=search_metadata,
    )


def export_collection(
    collection_type: str,
    collection_name: str,
    output_path: str = None,
) -> str:
    """
    Export a collection as a zip file.
    
    Args:
        collection_type: Type of collection ('artists' or 'styles')
        collection_name: Name of the collection
        output_path: Path to save the zip file (defaults to collection_name.zip)
    
    Returns:
        Path to the exported zip file
    """
    library = ReferenceLibrary()
    return library.export_collection(
        collection_type=collection_type,
        collection_name=collection_name,
        output_path=output_path,
    )


def import_collection(
    collection_type: str,
    collection_name: str,
    zip_path: str,
    overwrite: bool = False,
) -> Tuple[int, int]:
    """
    Import a collection from a zip file.
    
    Args:
        collection_type: Type of collection ('artists' or 'styles')
        collection_name: Name of the collection
        zip_path: Path to the zip file
        overwrite: If True, overwrite existing files
    
    Returns:
        Tuple of (number of files imported, number of files skipped)
    """
    library = ReferenceLibrary()
    return library.import_collection(
        collection_type=collection_type,
        collection_name=collection_name,
        zip_path=zip_path,
        overwrite=overwrite,
    )
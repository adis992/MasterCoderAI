import React, { useState, useEffect } from 'react';

function LibraryGallery() {
  const [images, setImages] = useState([]);
  const [columns, setColumns] = useState(4);

  useEffect(() => {
    fetch('https://chatgpt.com/library')
      .then(res => res.text())
      .then(html => {
        const doc = new DOMParser().parseFromString(html, 'text/html');
        const urls = Array.from(doc.querySelectorAll('img')).map(img => img.src);
        setImages(urls);
      })
      .catch(console.error);
  }, []);

  // Remove duplicate URLs
  const uniqueImages = Array.from(new Set(images));
  return (
    <>
      <div className="mb-4 flex items-center space-x-2">
        <label className="font-medium">Columns:</label>
        <select
          value={columns}
          onChange={e => setColumns(Number(e.target.value))}
          className="border rounded p-1"
        >
          {[2,3,4,6].map(n => (
            <option key={n} value={n}>{n}</option>
          ))}
        </select>
      </div>
      <div
        className="grid gap-4"
        style={{ gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))` }}
      >
        {uniqueImages.map(url => (
          <img
            key={url}
            src={url}
            alt="thumbnail"
            className="w-full h-auto rounded-lg shadow"
          />
        ))}
      </div>
    </>
  );
}

export default LibraryGallery;
"use client";

import { useState, useEffect } from "react";
import { UploadedFile } from "./DocumentsUpload";

interface Props {
  files: UploadedFile[];
}

export default function KnowledgeGraph({ files }: Props) {
  const [html, setHtml] = useState<string>("");

  useEffect(() => {
    fetch("/api/visualize")
      .then(res => res.text())
      .then(setHtml)
      .catch(console.error);
  }, [files]);

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-800">Knowledge Graph</h2>
      <div 
        className="w-full h-[600px] bg-white rounded-lg shadow"
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </div>
  );
}
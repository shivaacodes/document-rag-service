"use client";
import { useState } from "react";
import Header from "@/components/Header";
import dynamic from 'next/dynamic';
const PDFViewer = dynamic(() => import('@/components/PDFViewer'), { ssr: false });
import ChatInterface from "@/components/ChatInterface";
import { uploadDocument } from "@/lib/api";

export default function Home() {
  const [fileUrl, setFileUrl] = useState<string | undefined>(undefined);
  const [fileType, setFileType] = useState<string | undefined>(undefined);
  const [textContent, setTextContent] = useState<string | undefined>(undefined);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileUpload = async (file: File) => {
    // 1. Display locally immediately
    const url = URL.createObjectURL(file);
    setFileUrl(url);
    setFileType(file.type);

    if (file.type === 'text/plain') {
      const text = await file.text();
      setTextContent(text);
    } else {
      setTextContent(undefined);
    }

    // 2. Upload to backend
    setIsUploading(true);
    try {
      await uploadDocument(file);
      console.log("File uploaded successfully");
    } catch (error) {
      console.error("Upload failed", error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="flex h-screen flex-col bg-white font-sans dark:bg-black">
      <Header onFileUpload={handleFileUpload} />
      <main className="flex flex-1 overflow-hidden">
        <div className="w-[70%] bg-gray-50 dark:bg-black border-r border-gray-200 dark:border-gray-800">
          {fileType === 'text/plain' && textContent ? (
            <div className="p-8 h-full overflow-auto">
              <pre className="whitespace-pre-wrap font-mono text-sm text-gray-800 dark:text-gray-200">
                {textContent}
              </pre>
            </div>
          ) : (
            <PDFViewer fileUrl={fileUrl} />
          )}
        </div>
        <div className="w-[30%]">
          <ChatInterface />
        </div>
      </main>
    </div>
  );
}

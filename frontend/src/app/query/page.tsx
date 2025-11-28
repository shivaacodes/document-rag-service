"use client";
import { useState } from "react";
import Header from "@/components/Header";
import dynamic from 'next/dynamic';
const PDFViewer = dynamic(() => import('@/components/PDFViewer'), { ssr: false });
import ChatInterface from "@/components/ChatInterface";

export default function QueryPage() {
    const [fileUrl, setFileUrl] = useState<string | undefined>(undefined);

    // This might need to change if we are loading from backend, 
    // but for now keeping the structure compatible with the viewer.
    // In a real scenario, we might fetch the PDF blob from the backend 
    // using the document ID.

    const handleFileUpload = (file: File) => {
        const url = URL.createObjectURL(file);
        setFileUrl(url);
    };

    return (
        <div className="flex h-screen flex-col bg-white font-sans dark:bg-black">
            <Header onFileUpload={handleFileUpload} />
            <main className="flex flex-1 overflow-hidden">
                <div className="w-[70%]">
                    <PDFViewer fileUrl={fileUrl} />
                </div>
                <div className="w-[30%]">
                    <ChatInterface />
                </div>
            </main>
        </div>
    );
}

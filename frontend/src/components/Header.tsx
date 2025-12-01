"use client";
import React, { useRef } from 'react';
import { Upload } from 'lucide-react';

interface HeaderProps {
    onFileUpload?: (file: File) => void;
}

export default function Header({ onFileUpload }: HeaderProps) {
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleButtonClick = () => {
        fileInputRef.current?.click();
    };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file && onFileUpload) {
            onFileUpload(file);
        }
    };

    return (
        <header className="flex items-center justify-between border-b border-gray-200 bg-white px-6 py-4 dark:border-gray-800 dark:bg-black">
            {onFileUpload && (
                <>
                    <input
                        type="file"
                        ref={fileInputRef}
                        onChange={handleFileChange}
                        accept=".pdf,.txt"
                        className="hidden"
                    />
                    <button
                        onClick={handleButtonClick}
                        className="flex items-center gap-3 rounded-xl border border-gray-300 bg-white px-6 py-3 text-base font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-700 dark:bg-black dark:text-gray-300 dark:hover:bg-gray-900"
                    >
                        <Upload className="h-5 w-5" />
                        upload file
                    </button>
                </>
            )}
        </header>
    );
}

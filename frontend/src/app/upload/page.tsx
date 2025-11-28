"use client";
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Upload, FileText, Loader2 } from 'lucide-react';
import { uploadDocument } from '@/lib/api';

export default function UploadPage() {
    const router = useRouter();
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) return;

        setIsUploading(true);
        setError(null);

        try {
            await uploadDocument(file);
            // For now, we redirect to query. 
            // Ideally we'd pass the document ID or context.
            router.push('/query');
        } catch (err) {
            setError('Failed to upload document. Please try again.');
            console.error(err);
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="flex h-screen flex-col items-center justify-center bg-white font-sans dark:bg-black">
            <div className="w-full max-w-md space-y-8 px-4">
                <div className="text-center">
                    <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white">
                        Upload Document
                    </h1>
                    <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                        Upload a PDF or TXT file to start querying.
                    </p>
                </div>

                <div className="group relative mt-8 flex min-h-[200px] cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-gray-300 bg-gray-50 transition-colors hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-900/50 dark:hover:bg-gray-900">
                    <input
                        type="file"
                        className="absolute inset-0 z-10 h-full w-full cursor-pointer opacity-0"
                        onChange={handleFileChange}
                        accept=".pdf,.txt"
                        disabled={isUploading}
                    />

                    {isUploading ? (
                        <div className="flex flex-col items-center gap-2">
                            <Loader2 className="h-10 w-10 animate-spin text-gray-400" />
                            <p className="text-sm font-medium text-gray-500">Uploading...</p>
                        </div>
                    ) : (
                        <div className="flex flex-col items-center gap-2 text-center">
                            <div className="rounded-full bg-gray-100 p-4 dark:bg-gray-800">
                                <Upload className="h-8 w-8 text-gray-500 dark:text-gray-400" />
                            </div>
                            <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                Click to upload or drag and drop
                            </p>
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                                PDF or TXT (max 10MB)
                            </p>
                        </div>
                    )}
                </div>

                {error && (
                    <div className="rounded-lg bg-red-50 p-4 text-sm text-red-800 dark:bg-red-900/10 dark:text-red-200">
                        {error}
                    </div>
                )}
            </div>
        </div>
    );
}

'use client';

import { useState, useEffect } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import { ZoomIn, ZoomOut, ChevronLeft, ChevronRight } from 'lucide-react';

// Configure PDF worker
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

export default function PDFViewer({ fileUrl }: { fileUrl?: string }) {
    const [numPages, setNumPages] = useState<number>(0);
    const [pageNumber, setPageNumber] = useState<number>(1);
    const [scale, setScale] = useState<number>(1.0);

    // Reset page number when file changes
    useEffect(() => {
        setPageNumber(1);
    }, [fileUrl]);

    function onDocumentLoadSuccess({ numPages }: { numPages: number }) {
        setNumPages(numPages);
    }

    return (
        <div className="flex h-full flex-col border-r border-gray-200 bg-gray-50 dark:border-gray-800 dark:bg-black">
            <div className="flex items-center justify-between border-b border-gray-200 p-4 dark:border-gray-800">
                {/* Zoom Controls */}
                <div className="flex items-center gap-4">
                    <button
                        onClick={() => setScale((prev) => Math.max(0.5, prev - 0.1))}
                        className="rounded-lg p-2 hover:bg-gray-200 dark:hover:bg-gray-800"
                        title="Zoom Out"
                    >
                        <ZoomOut className="h-5 w-5" />
                    </button>
                    <span className="text-sm font-medium text-gray-600 dark:text-gray-400 w-12 text-center">
                        {Math.round(scale * 100)}%
                    </span>
                    <button
                        onClick={() => setScale((prev) => Math.min(2.0, prev + 0.1))}
                        className="rounded-lg p-2 hover:bg-gray-200 dark:hover:bg-gray-800"
                        title="Zoom In"
                    >
                        <ZoomIn className="h-5 w-5" />
                    </button>
                </div>

                {/* Page Navigation */}
                <div className="flex items-center gap-4">
                    <button
                        onClick={() => setPageNumber((prev) => Math.max(1, prev - 1))}
                        disabled={pageNumber <= 1}
                        className="rounded-lg p-2 hover:bg-gray-200 disabled:opacity-30 dark:hover:bg-gray-800"
                        title="Previous Page"
                    >
                        <ChevronLeft className="h-5 w-5" />
                    </button>
                    <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                        Page {pageNumber} of {numPages || '--'}
                    </span>
                    <button
                        onClick={() => setPageNumber((prev) => Math.min(numPages, prev + 1))}
                        disabled={pageNumber >= numPages}
                        className="rounded-lg p-2 hover:bg-gray-200 disabled:opacity-30 dark:hover:bg-gray-800"
                        title="Next Page"
                    >
                        <ChevronRight className="h-5 w-5" />
                    </button>
                </div>
            </div>

            <div className="flex-1 overflow-auto p-4">
                <div className="flex justify-center">
                    {fileUrl ? (
                        <Document
                            file={fileUrl}
                            onLoadSuccess={onDocumentLoadSuccess}
                            className="shadow-lg"
                        >
                            <Page
                                pageNumber={pageNumber}
                                scale={scale}
                                renderTextLayer={false}
                                renderAnnotationLayer={false}
                            />
                        </Document>
                    ) : (
                        <div className="flex h-full flex-col items-center justify-center text-gray-400">
                            <p className="text-xl">No document loaded</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

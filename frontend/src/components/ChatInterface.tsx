import { useState, useRef, useEffect } from 'react';
import { Send, Loader2, Bot } from 'lucide-react';
import { motion } from 'framer-motion';
import { queryDocument } from '@/lib/api';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    context?: string;
}

const Typewriter = ({ text }: { text: string }) => {
    const words = text.split(/(\s+)/);
    return (
        <span className="whitespace-pre-wrap">
            {words.map((word, i) => (
                <motion.span
                    key={i}
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.1, delay: i * 0.015 }}
                >
                    {word}
                </motion.span>
            ))}
        </span>
    );
};

export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const data = await queryDocument(userMessage);
            setMessages((prev) => [
                ...prev,
                {
                    role: 'assistant',
                    content: data.answer,
                    context: data.chunks && data.chunks.length > 0 ? data.chunks[0].text : undefined,
                },
            ]);
        } catch (error) {
            console.error('Failed to query document:', error);
            setMessages((prev) => [
                ...prev,
                { role: 'assistant', content: `Error: ${error instanceof Error ? error.message : 'Unknown error'}` },
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex h-full flex-col bg-white dark:bg-black">
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-6">
                {messages.length === 0 ? (
                    <div className="flex h-full flex-col items-center justify-center text-center text-gray-500">
                        <Bot className="mb-4 h-12 w-12 opacity-20" />
                        <p className="text-lg font-medium">Ask questions about your document</p>
                    </div>
                ) : (
                    <div className="space-y-8">
                        {messages.map((msg, index) => (
                            <div key={index} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                                <motion.div
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ duration: 0.4, ease: "easeOut" }}
                                    className={`max-w-[90%] rounded-2xl text-lg leading-relaxed ${msg.role === 'user'
                                        ? 'bg-black text-white dark:bg-white dark:text-black px-6 py-4'
                                        : 'text-gray-900 dark:text-gray-100 py-2'
                                        }`}
                                >
                                    {msg.role === 'assistant' ? (
                                        <Typewriter text={msg.content} />
                                    ) : (
                                        msg.content
                                    )}
                                </motion.div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="flex items-start">
                                <div className="py-3">
                                    <Loader2 className="h-6 w-6 animate-spin text-gray-500" />
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>
                )}
            </div>

            {/* Input Area */}
            <div className="border-t border-gray-200 p-6 dark:border-gray-800">
                <div className="relative">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask a question..."
                        disabled={isLoading}
                        className="w-full rounded-xl border border-gray-300 bg-white px-6 py-4 pr-14 text-lg focus:border-black focus:outline-none disabled:opacity-50 dark:border-gray-700 dark:bg-black dark:focus:border-white"
                    />
                    <button
                        onClick={handleSend}
                        disabled={!input.trim() || isLoading}
                        className="absolute right-3 top-1/2 -translate-y-1/2 rounded-lg p-2 text-gray-500 hover:bg-gray-100 hover:text-black disabled:opacity-50 dark:hover:bg-gray-900 dark:hover:text-white"
                    >
                        <Send className="h-6 w-6" />
                    </button>
                </div>
            </div>
        </div>
    );
}

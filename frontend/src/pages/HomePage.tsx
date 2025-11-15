import { useState } from "react";
import { ChatMessage } from "@/components/custom/ChatMessage";
import { ChatInput } from "@/components/custom/ChatInput";
import { ChatHeader } from "@/components/custom/ChatHeader";
// import { AppSidebar } from "@/components/custom/AppSidebar";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export const HomePage = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hello! How can I help you today?",
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState("gpt-4");

  const handleReset = () => {
    setMessages([
      {
        id: "1",
        role: "assistant",
        content: "Hello! How can I help you today?",
      },
    ]);
  };

  const handleSendMessage = (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // Simulate AI response
    // TODO: Send request to back
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          "This is a simulated response. In a real application, this would be connected to an AI backend.",
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 1000);
  };

  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full bg-background">
        {/* <AppSidebar
          onReset={handleReset}
          selectedModel={selectedModel}
          onModelChange={setSelectedModel}
        /> */}

        <div className="flex flex-col flex-1 h-screen">
          <header className="h-12 flex items-center border-b border-border">
            <SidebarTrigger className="ml-2" />
            <ChatHeader />
          </header>

          <div className="flex-1 overflow-y-auto">
            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                role={message.role}
                content={message.content}
              />
            ))}
            {isLoading && <ChatMessage role="assistant" content="Typing..." />}
          </div>

          <ChatInput onSend={handleSendMessage} disabled={isLoading} />
        </div>
      </div>
    </SidebarProvider>
  );
};

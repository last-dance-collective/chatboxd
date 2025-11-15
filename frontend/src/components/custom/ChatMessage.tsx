import { cn } from "@/lib/utils";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
}

export const ChatMessage = ({ role, content }: ChatMessageProps) => {
  return (
    <div
      className={cn(
        "flex w-full py-6 px-4",
        role === "assistant" ? "bg-secondary/50" : ""
      )}
    >
      <div className="max-w-3xl w-full mx-auto flex gap-4">
        <div
          className={cn(
            "shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium",
            role === "user"
              ? "bg-chat-user-bg text-chat-user-fg"
              : "bg-muted text-muted-foreground"
          )}
        >
          {role === "user" ? "U" : "AI"}
        </div>
        <div className="flex-1 prose prose-invert max-w-none">
          <p className="text-foreground leading-relaxed whitespace-pre-wrap m-0">
            {content}
          </p>
        </div>
      </div>
    </div>
  );
};

import { RotateCcw } from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuItem,
  SidebarTrigger,
  useSidebar,
} from "@/components/ui/sidebar";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface SidebarCustomProps {
  onReset: () => void;
  selectedModel: string;
  onModelChange: (model: string) => void;
}

const AI_MODELS = [
  { value: "gpt-4", label: "GPT-4" },
  { value: "gpt-3.5-turbo", label: "GPT-3.5 Turbo" },
  { value: "claude-3", label: "Claude 3" },
  { value: "gemini-pro", label: "Gemini Pro" },
];

export const SidebarCustom = ({
  onReset,
  selectedModel,
  onModelChange,
}: SidebarCustomProps) => {
  const { state } = useSidebar();
  const collapsed = state === "collapsed";
  return (
    <Sidebar className={collapsed ? "w-14" : "w-64"}>
      <SidebarTrigger className="m-2 self-end" />
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Chat Settings</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <div className="px-2 py-2 space-y-4">
                  {!collapsed && (
                    <>
                      <div className="space-y-2">
                        <label className="text-xs font-medium text-muted-foreground">
                          AI Model
                        </label>
                        <Select value={selectedModel} onValueChange={onModelChange}>
                          <SelectTrigger className="w-full">
                            <SelectValue placeholder="Select model" />
                          </SelectTrigger>
                          <SelectContent>
                            {AI_MODELS.map((model) => (
                              <SelectItem key={model.value} value={model.value}>
                                {model.label}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      <Button onClick={onReset} variant="outline" className="w-full">
                        <RotateCcw className="mr-2 h-4 w-4" />
                        Reset Conversation
                      </Button>
                    </>
                  )}
                  {collapsed && (
                    <Button
                      onClick={onReset}
                      variant="outline"
                      size="icon"
                      className="w-full"
                    >
                      <RotateCcw className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
};

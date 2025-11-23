import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { YourTwin } from './YourTwin';
import { FriendsFeed } from './FriendsFeed';
import { Button } from './ui/button';

interface DashboardProps {
  answers: Record<string, string>;
  onRetake: () => void;
}

export function Dashboard({ answers, onRetake }: DashboardProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-50">
      <div className="bg-[#6D3F1F] text-white py-8 px-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-4xl mb-2">Your Restaurant Twin Results</h1>
            <p className="text-amber-100">
              Discover restaurants perfectly matched to your taste
            </p>
          </div>
          <Button onClick={onRetake} variant="outline" className="bg-white text-[#6D3F1F] hover:bg-amber-50">
            Retake Quiz
          </Button>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <Tabs defaultValue="your-twin" className="space-y-6">
          <TabsList className="grid w-full max-w-md mx-auto grid-cols-2 bg-[#6D3F1F]/10">
            <TabsTrigger value="your-twin" className="data-[state=active]:bg-[#6D3F1F] data-[state=active]:text-white">
              Your Twin
            </TabsTrigger>
            <TabsTrigger value="friends" className="data-[state=active]:bg-[#6D3F1F] data-[state=active]:text-white">
              Friends
            </TabsTrigger>
          </TabsList>

          <TabsContent value="your-twin" className="space-y-6">
            <YourTwin answers={answers} />
          </TabsContent>

          <TabsContent value="friends" className="space-y-6">
            <FriendsFeed />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}

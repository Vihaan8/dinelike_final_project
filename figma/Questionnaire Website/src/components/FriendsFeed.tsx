import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from './ui/dialog';
import { Star, MapPin, Users } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface Friend {
  id: string;
  name: string;
  avatar: string;
  twinName: string;
  twinAvatar: string;
  matchScore: number;
  timeTaken: string;
  location: string;
  sharedRestaurants: Restaurant[];
}

interface Restaurant {
  name: string;
  image: string;
  cuisine: string;
  rating: number;
  priceRange: string;
  location: string;
  whyRecommended: string;
}

const friendsData: Friend[] = [
  {
    id: '1',
    name: 'Alex K.',
    avatar: 'https://images.unsplash.com/photo-1672072961782-7ff336a621bf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxoYXBweSUyMHBlcnNvbiUyMGZvb2R8ZW58MXx8fHwxNzYzNjgwOTUwfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
    twinName: 'Jordan P.',
    twinAvatar: 'https://images.unsplash.com/photo-1663470477088-7d83eb03d021?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwZXJzb24lMjByZXN0YXVyYW50fGVufDF8fHx8MTc2MzY4MDk1MHww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
    matchScore: 91,
    timeTaken: '2 minutes ago',
    location: 'Oakland, CA',
    sharedRestaurants: [
      {
        name: 'Commis',
        image: 'https://images.unsplash.com/photo-1648462908676-8305f0eff8e0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjYWZlJTIwaW50ZXJpb3J8ZW58MXx8fHwxNzYzNTk3MzM1fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        cuisine: 'Contemporary American',
        rating: 4.8,
        priceRange: '$$$$',
        location: 'Oakland',
        whyRecommended: 'Perfect for Alex\'s fine dining preference and Jordan\'s adventurous palate'
      },
      {
        name: 'Homeroom',
        image: 'https://images.unsplash.com/photo-1686836715835-65af22ea5cd4?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxiaXN0cm8lMjByZXN0YXVyYW50fGVufDF8fHx8MTc2MzY4MDk1M3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        cuisine: 'Comfort Food',
        rating: 4.4,
        priceRange: '$$',
        location: 'Oakland',
        whyRecommended: 'Matches both their love for comfort food with a creative twist'
      }
    ]
  },
  {
    id: '2',
    name: 'Maria S.',
    avatar: 'https://images.unsplash.com/photo-1677126473160-cdfb24dfdf78?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwZXJzb24lMjBkaW5pbmd8ZW58MXx8fHwxNzYzNjgwOTUwfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
    twinName: 'Chris L.',
    twinAvatar: 'https://images.unsplash.com/photo-1672462478040-a5920e2c23d8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwZXJzb24lMjBzbWlsaW5nJTIwcG9ydHJhaXR8ZW58MXx8fHwxNzYzNjA0NDM1fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
    matchScore: 88,
    timeTaken: '15 minutes ago',
    location: 'Berkeley, CA',
    sharedRestaurants: [
      {
        name: 'Chez Panisse',
        image: 'https://images.unsplash.com/photo-1532117472055-4d0734b51f31?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxpdGFsaWFuJTIwcmVzdGF1cmFudHxlbnwxfHx8fDE3NjM1OTI2MzN8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        cuisine: 'Californian',
        rating: 4.9,
        priceRange: '$$$$',
        location: 'Berkeley',
        whyRecommended: 'Legendary farm-to-table restaurant matching their organic food preferences'
      },
      {
        name: 'Ippuku',
        image: 'https://images.unsplash.com/photo-1696449241254-11cf7f18ce32?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzdXNoaSUyMHJlc3RhdXJhbnR8ZW58MXx8fHwxNzYzNjExMjA3fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        cuisine: 'Japanese Izakaya',
        rating: 4.6,
        priceRange: '$$$',
        location: 'Berkeley',
        whyRecommended: 'Authentic izakaya experience perfect for sharing small plates'
      }
    ]
  },
  {
    id: '3',
    name: 'James T.',
    avatar: 'https://images.unsplash.com/photo-1663470477088-7d83eb03d021?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwZXJzb24lMjByZXN0YXVyYW50fGVufDF8fHx8MTc2MzY4MDk1MHww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
    twinName: 'Emma W.',
    twinAvatar: 'https://images.unsplash.com/photo-1672072961782-7ff336a621bf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxoYXBweSUyMHBlcnNvbiUyMGZvb2R8ZW58MXx8fHwxNzYzNjgwOTUwfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
    matchScore: 93,
    timeTaken: '1 hour ago',
    location: 'San Jose, CA',
    sharedRestaurants: [
      {
        name: 'Adega',
        image: 'https://images.unsplash.com/photo-1653084019129-1f2303bb5bc0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZXhpY2FuJTIwcmVzdGF1cmFudHxlbnwxfHx8fDE3NjM2NDEzNjl8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        cuisine: 'Portuguese',
        rating: 4.7,
        priceRange: '$$$',
        location: 'San Jose',
        whyRecommended: 'Upscale Portuguese cuisine matching their Mediterranean preferences'
      },
      {
        name: 'Gochi Japanese Fusion',
        image: 'https://images.unsplash.com/photo-1710846929339-72634edf6f5f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxyZXN0YXVyYW50JTIwZXh0ZXJpb3J8ZW58MXx8fHwxNzYzNjY1MTc3fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
        cuisine: 'Japanese Fusion',
        rating: 4.5,
        priceRange: '$$$',
        location: 'Cupertino',
        whyRecommended: 'Creative fusion dishes that blend traditional and modern flavors'
      }
    ]
  }
];

export function FriendsFeed() {
  const [selectedFriend, setSelectedFriend] = useState<Friend | null>(null);

  return (
    <>
      <div>
        <div className="bg-[#6D3F1F] text-white p-6 rounded-lg mb-6">
          <div className="flex items-center gap-2 mb-2">
            <Users className="w-6 h-6" />
            <h3 className="text-2xl">Live Feed</h3>
          </div>
          <p className="text-amber-100">See who else just found their restaurant twin!</p>
        </div>

        <div className="space-y-4">
          {friendsData.map((friend) => (
            <Card
              key={friend.id}
              className="cursor-pointer hover:shadow-lg transition-all hover:border-[#6D3F1F]/40"
              onClick={() => setSelectedFriend(friend)}
            >
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="flex items-center -space-x-2">
                      <ImageWithFallback
                        src={friend.avatar}
                        alt={friend.name}
                        className="w-12 h-12 rounded-full border-2 border-white object-cover relative z-10"
                      />
                      <ImageWithFallback
                        src={friend.twinAvatar}
                        alt={friend.twinName}
                        className="w-12 h-12 rounded-full border-2 border-white object-cover"
                      />
                    </div>
                    <div>
                      <CardTitle className="text-lg">
                        {friend.name} + {friend.twinName}
                      </CardTitle>
                      <CardDescription className="flex items-center gap-2">
                        <span className="flex items-center gap-1">
                          <MapPin className="w-3 h-3" />
                          {friend.location}
                        </span>
                        <span>•</span>
                        <span>{friend.timeTaken}</span>
                      </CardDescription>
                    </div>
                  </div>
                  <Badge className="bg-[#6D3F1F]">
                    {friend.matchScore}% Match
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-600">
                  Click to see their personalized restaurant recommendations
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Modal */}
      <Dialog open={!!selectedFriend} onOpenChange={() => setSelectedFriend(null)}>
        <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
          {selectedFriend && (
            <>
              <DialogHeader>
                <DialogTitle className="text-2xl flex items-center gap-3">
                  <div className="flex items-center -space-x-2">
                    <ImageWithFallback
                      src={selectedFriend.avatar}
                      alt={selectedFriend.name}
                      className="w-10 h-10 rounded-full border-2 border-white object-cover relative z-10"
                    />
                    <ImageWithFallback
                      src={selectedFriend.twinAvatar}
                      alt={selectedFriend.twinName}
                      className="w-10 h-10 rounded-full border-2 border-white object-cover"
                    />
                  </div>
                  <span>
                    {selectedFriend.name} & {selectedFriend.twinName}
                  </span>
                </DialogTitle>
                <DialogDescription>
                  Recommended restaurants for this twin pair in {selectedFriend.location}
                </DialogDescription>
              </DialogHeader>

              <div className="grid md:grid-cols-2 gap-4 mt-4">
                {selectedFriend.sharedRestaurants.map((restaurant, index) => (
                  <Card key={index} className="overflow-hidden">
                    <div className="aspect-video relative">
                      <ImageWithFallback
                        src={restaurant.image}
                        alt={restaurant.name}
                        className="w-full h-full object-cover"
                      />
                      <Badge className="absolute top-3 right-3 bg-[#6D3F1F]">
                        {restaurant.priceRange}
                      </Badge>
                    </div>
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div>
                          <CardTitle className="text-lg">{restaurant.name}</CardTitle>
                          <CardDescription className="flex items-center gap-1 mt-1">
                            <MapPin className="w-3 h-3" />
                            {restaurant.location}
                          </CardDescription>
                        </div>
                        <div className="flex items-center gap-1">
                          <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                          <span className="font-semibold">{restaurant.rating}</span>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-slate-600 mb-2">{restaurant.cuisine}</p>
                      <p className="text-sm bg-amber-50 p-3 rounded border-l-4 border-[#6D3F1F]">
                        {restaurant.whyRecommended}
                      </p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </>
  );
}

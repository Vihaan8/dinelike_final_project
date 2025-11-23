import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Star, ThumbsUp, ThumbsDown, MapPin } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface YourTwinProps {
  answers: Record<string, string>;
}

// Mock twin data
const twinData = {
  name: 'Sarah M.',
  avatar: 'https://images.unsplash.com/photo-1672462478040-a5920e2c23d8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwZXJzb24lMjBzbWlsaW5nJTIwcG9ydHJhaXR8ZW58MXx8fHwxNzYzNjA0NDM1fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
  matchScore: 94,
  location: 'San Francisco, CA',
  reviewCount: 247,
  goodReviews: [
    {
      restaurant: 'La Ciccia',
      rating: 5,
      review: 'Absolutely incredible authentic Sardinian cuisine! The pasta was handmade and perfectly cooked. The wine selection complemented every dish beautifully. Cozy atmosphere makes you feel like you\'re in Italy.',
      date: '2 weeks ago'
    },
    {
      restaurant: 'Burma Superstar',
      rating: 5,
      review: 'The tea leaf salad is a must-try! Perfectly balanced flavors and the samosas were crispy and delicious. Great for sharing multiple dishes with friends. Service was attentive without being intrusive.',
      date: '1 month ago'
    },
    {
      restaurant: 'Tartine Bakery',
      rating: 5,
      review: 'Best morning croissants in the city! The butter is phenomenal and the coffee is always perfect. Worth the wait in line. The bread pudding is also divine - not too sweet, just right.',
      date: '3 weeks ago'
    }
  ],
  badReviews: [
    {
      restaurant: 'The Overpriced Spot',
      rating: 2,
      review: 'Extremely disappointed. Portions were tiny for the price and the food was underwhelming. The ambiance was trying too hard to be fancy. Service was slow and inattentive. Would not return.',
      date: '2 months ago'
    },
    {
      restaurant: 'Fusion Confusion',
      rating: 1,
      review: 'The concept sounded interesting but execution was terrible. Flavors didn\'t work together at all. Everything tasted like it came out of a microwave. Save your money and go literally anywhere else.',
      date: '3 months ago'
    }
  ]
};

const recommendations = [
  {
    name: 'Nopa',
    image: 'https://images.unsplash.com/photo-1710846929339-72634edf6f5f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxyZXN0YXVyYW50JTIwZXh0ZXJpb3J8ZW58MXx8fHwxNzYzNjY1MTc3fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
    cuisine: 'California Cuisine',
    rating: 4.5,
    priceRange: '$$$',
    matchReason: 'Based on your love for farm-to-table and casual fine dining',
    location: 'Alamo Square'
  },
  {
    name: 'State Bird Provisions',
    image: 'https://images.unsplash.com/photo-1532117472055-4d0734b51f31?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxpdGFsaWFuJTIwcmVzdGF1cmFudHxlbnwxfHx8fDE3NjM1OTI2MzN8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
    cuisine: 'American (New)',
    rating: 4.7,
    priceRange: '$$$',
    matchReason: 'Your twin rated this 5 stars - innovative small plates',
    location: 'Western Addition'
  },
  {
    name: 'Kin Khao',
    image: 'https://images.unsplash.com/photo-1696449241254-11cf7f18ce32?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzdXNoaSUyMHJlc3RhdXJhbnR8ZW58MXx8fHwxNzYzNjExMjA3fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
    cuisine: 'Thai',
    rating: 4.6,
    priceRange: '$$',
    matchReason: 'Matches your preference for bold, spicy flavors',
    location: 'Union Square'
  },
  {
    name: 'Delfina',
    image: 'https://images.unsplash.com/photo-1653084019129-1f2303bb5bc0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZXhpY2FuJTIwcmVzdGF1cmFudHxlbnwxfHx8fDE3NjM2NDEzNjl8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
    cuisine: 'Italian',
    rating: 4.6,
    priceRange: '$$$',
    matchReason: 'Perfect for your Italian cuisine preference',
    location: 'Mission District'
  }
];

export function YourTwin({ answers }: YourTwinProps) {
  return (
    <div className="space-y-8">
      {/* Twin Profile */}
      <Card className="overflow-hidden border-2 border-[#6D3F1F]/20">
        <div className="bg-gradient-to-r from-[#6D3F1F] to-[#8B5A3C] p-6 text-white">
          <div className="flex items-center gap-6">
            <div className="relative">
              <ImageWithFallback
                src={twinData.avatar}
                alt={twinData.name}
                className="w-24 h-24 rounded-full border-4 border-white object-cover"
              />
              <Badge className="absolute -bottom-2 left-1/2 -translate-x-1/2 bg-green-500 border-white">
                {twinData.matchScore}% Match
              </Badge>
            </div>
            <div className="flex-1">
              <h2 className="text-3xl mb-1">Meet Your Twin: {twinData.name}</h2>
              <div className="flex items-center gap-4 text-amber-100">
                <span className="flex items-center gap-1">
                  <MapPin className="w-4 h-4" />
                  {twinData.location}
                </span>
                <span>{twinData.reviewCount} Yelp reviews</span>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Good Reviews */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <ThumbsUp className="w-6 h-6 text-green-600" />
          <h3 className="text-2xl">What {twinData.name.split(' ')[0]} Loves</h3>
        </div>
        <div className="grid gap-4">
          {twinData.goodReviews.map((review, index) => (
            <Card key={index} className="border-l-4 border-l-green-500">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">{review.restaurant}</CardTitle>
                  <div className="flex items-center gap-1">
                    {[...Array(review.rating)].map((_, i) => (
                      <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                    ))}
                  </div>
                </div>
                <CardDescription>{review.date}</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-slate-700">{review.review}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Bad Reviews */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <ThumbsDown className="w-6 h-6 text-red-600" />
          <h3 className="text-2xl">What {twinData.name.split(' ')[0]} Avoids</h3>
        </div>
        <div className="grid gap-4">
          {twinData.badReviews.map((review, index) => (
            <Card key={index} className="border-l-4 border-l-red-500 bg-red-50/30">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">{review.restaurant}</CardTitle>
                  <div className="flex items-center gap-1">
                    {[...Array(review.rating)].map((_, i) => (
                      <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                    ))}
                    {[...Array(5 - review.rating)].map((_, i) => (
                      <Star key={i} className="w-4 h-4 text-gray-300" />
                    ))}
                  </div>
                </div>
                <CardDescription>{review.date}</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-slate-700">{review.review}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Recommendations */}
      <div>
        <div className="bg-[#6D3F1F] text-white p-6 rounded-lg mb-4">
          <h3 className="text-2xl mb-2">Restaurants We Think You'll Love</h3>
          <p className="text-amber-100">Based on your quiz answers and your twin's preferences</p>
        </div>
        <div className="grid md:grid-cols-2 gap-6">
          {recommendations.map((restaurant, index) => (
            <Card key={index} className="overflow-hidden hover:shadow-lg transition-shadow">
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
                    <CardTitle>{restaurant.name}</CardTitle>
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
                  {restaurant.matchReason}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

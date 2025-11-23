import { useState } from 'react';
import { Button } from './ui/button';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { Dashboard } from './Dashboard';

interface Option {
  id: string;
  label: string;
  image: string;
}

interface Question {
  id: string;
  title: string;
  options: Option[];
}

const quizData: Question[] = [
  {
    id: 'cuisine',
    title: 'Pick your favorite cuisine!',
    options: [
      { id: 'italian', label: 'Italian', image: 'https://images.unsplash.com/photo-1588013273468-315fd88ea34c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwYXN0YSUyMGNhcmJvbmFyYXxlbnwxfHx8fDE3NjM2MjkzMDh8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'mexican', label: 'Mexican', image: 'https://images.unsplash.com/photo-1595531401542-d0bb33afbfbe?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0YWNvcyUyMG1leGljYW58ZW58MXx8fHwxNzYzNjUwODQ4fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'asian', label: 'Asian', image: 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxyYW1lbiUyMG5vb2RsZXN8ZW58MXx8fHwxNzYzNTkyNzQ1fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'indian', label: 'Indian', image: 'https://images.unsplash.com/photo-1710091691802-7dedb8af9a77?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxpbmRpYW4lMjBjdXJyeXxlbnwxfHx8fDE3NjM2MzIzODB8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'mediterranean', label: 'Mediterranean', image: 'https://images.unsplash.com/photo-1653611540493-b3a896319fbf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZWRpdGVycmFuZWFuJTIwZm9vZHxlbnwxfHx8fDE3NjM2NTAwOTR8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'american', label: 'American', image: 'https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxidXJnZXIlMjBmcmllc3xlbnwxfHx8fDE3NjM2NTU1MTF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
    ],
  },
  {
    id: 'atmosphere',
    title: 'What kind of dining atmosphere do you prefer?',
    options: [
      { id: 'fine-dining', label: 'Fine dining', image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmaW5lJTIwZGluaW5nJTIwcmVzdGF1cmFudHxlbnwxfHx8fDE3NjM1NzU1ODd8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'casual-cafe', label: 'Casual cafe', image: 'https://images.unsplash.com/photo-1723986534763-b3fd65c75f0c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjYXN1YWwlMjBjYWZlfGVufDF8fHx8MTc2MzY3NzY1NXww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'food-truck', label: 'Food truck', image: 'https://images.unsplash.com/photo-1574028742226-ee1ab3520a7f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmb29kJTIwdHJ1Y2slMjBzdHJlZXR8ZW58MXx8fHwxNzYzNjMwNjQxfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'cozy-intimate', label: 'Cozy & intimate', image: 'https://images.unsplash.com/photo-1646473315764-c6cd47fe74c3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb3p5JTIwcmVzdGF1cmFudHxlbnwxfHx8fDE3NjM2Nzc2NTZ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'rooftop-views', label: 'Rooftop with views', image: 'https://images.unsplash.com/photo-1621275471769-e6aa344546d5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxyb29mdG9wJTIwcmVzdGF1cmFudHxlbnwxfHx8fDE3NjM2Nzc2NTZ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'family-friendly', label: 'Family friendly', image: 'https://images.unsplash.com/photo-1533777419517-3e4017e2e15a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmYW1pbHklMjByZXN0YXVyYW50fGVufDF8fHx8MTc2MzY3NzY1N3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
    ],
  },
  {
    id: 'protein',
    title: 'Choose your go-to protein!',
    options: [
      { id: 'steak', label: 'Steak', image: 'https://images.unsplash.com/photo-1706650616334-97875fae8521?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzdGVhayUyMGRpbm5lcnxlbnwxfHx8fDE3NjM1ODI0NjV8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'chicken', label: 'Chicken', image: 'https://images.unsplash.com/photo-1569058242253-92a9c755a0ec?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmcmllZCUyMGNoaWNrZW58ZW58MXx8fHwxNzYzNTgyODIzfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'seafood', label: 'Seafood', image: 'https://images.unsplash.com/photo-1519351635902-7c60d09cb2ed?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzZWFmb29kJTIwcGxhdHRlcnxlbnwxfHx8fDE3NjM2NDk0MTZ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'pork', label: 'Pork/BBQ', image: 'https://images.unsplash.com/photo-1544025162-d76694265947?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxiYnElMjByaWJzfGVufDF8fHx8MTc2MzYzODAzMHww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'vegetarian', label: 'Vegetarian', image: 'https://images.unsplash.com/photo-1623428187969-5da2dcea5ebf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx2ZWdhbiUyMHNhbGFkfGVufDF8fHx8MTc2MzY3NzY1N3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'variety', label: 'Mix of everything', image: 'https://images.unsplash.com/photo-1691995989456-6a77273f9f0c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkaW0lMjBzdW18ZW58MXx8fHwxNzYzNjA1NTU1fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
    ],
  },
  {
    id: 'spice',
    title: 'How do you like your spice level?',
    options: [
      { id: 'extra-spicy', label: 'Extra spicy!', image: 'https://images.unsplash.com/photo-1681264378210-055afa3b3a19?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzcGljeSUyMGhvdCUyMGZvb2R8ZW58MXx8fHwxNzYzNjc3NjYwfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'medium', label: 'Medium heat', image: 'https://images.unsplash.com/photo-1562565652-a0d8f0c59eb4?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0aGFpJTIwZm9vZHxlbnwxfHx8fDE3NjM2NTExNzV8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'mild', label: 'Mild & comfortable', image: 'https://images.unsplash.com/photo-1614597328441-2628a5169cb9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtaWxkJTIwY29tZm9ydCUyMGZvb2R8ZW58MXx8fHwxNzYzNjc3NjYwfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'no-spice', label: 'No spice please', image: 'https://images.unsplash.com/photo-1484723091739-30a097e8f929?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmcmVuY2glMjB0b2FzdHxlbnwxfHx8fDE3NjM2NzU0NDV8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'korean-spicy', label: 'Korean spicy', image: 'https://images.unsplash.com/photo-1632558610168-8377309e34c7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxrb3JlYW4lMjBiYnF8ZW58MXx8fHwxNzYzNTc2NDA1fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'varies', label: 'Depends on mood', image: 'https://images.unsplash.com/photo-1750271328082-22490577fbb5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxleG90aWMlMjBmb29kJTIwcGxhdHRlcnxlbnwxfHx8fDE3NjM2Nzc2NjF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
    ],
  },
  {
    id: 'drink',
    title: 'What are you drinking with your meal?',
    options: [
      { id: 'wine', label: 'Wine', image: 'https://images.unsplash.com/photo-1634832296440-b5bac2df86c3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3aW5lJTIwZ2xhc3N8ZW58MXx8fHwxNzYzNjU3MjkyfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'cocktails', label: 'Cocktails', image: 'https://images.unsplash.com/photo-1598994671512-395d7a6147e0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb2NrdGFpbCUyMGJhcnxlbnwxfHx8fDE3NjM1NzczMDF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'beer', label: 'Beer', image: 'https://images.unsplash.com/photo-1546622891-02c72c1537b6?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxiZWVyJTIwcHVifGVufDF8fHx8MTc2MzY3NzY2Mnww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'coffee', label: 'Coffee', image: 'https://images.unsplash.com/photo-1585494156145-1c60a4fe952b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb2ZmZWUlMjBsYXR0ZXxlbnwxfHx8fDE3NjM2MDk3NzF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'tea', label: 'Tea', image: 'https://images.unsplash.com/photo-1610478506025-8110cc8f1986?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZWElMjBjdXB8ZW58MXx8fHwxNzYzNjMzMTIyfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'juice', label: 'Fresh juice', image: 'https://images.unsplash.com/photo-1497534446932-c925b458314e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmcmVzaCUyMGp1aWNlfGVufDF8fHx8MTc2MzYwMjQyNHww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
    ],
  },
  {
    id: 'meal-time',
    title: 'When do you prefer to eat out?',
    options: [
      { id: 'breakfast', label: 'Breakfast/Brunch', image: 'https://images.unsplash.com/photo-1550582078-1549c4b3814f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxicmVha2Zhc3QlMjBicnVuY2h8ZW58MXx8fHwxNzYzNjE2MzM2fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'lunch', label: 'Lunch', image: 'https://images.unsplash.com/photo-1590301155505-471f05cd02db?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxsdW5jaCUyMHNhbmR3aWNofGVufDF8fHx8MTc2MzY3NzY2M3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'dinner', label: 'Dinner', image: 'https://images.unsplash.com/photo-1542557497-4c7b03d0d245?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxyb21hbnRpYyUyMGRpbm5lcnxlbnwxfHx8fDE3NjM2Nzc2NjN8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'late-night', label: 'Late night', image: 'https://images.unsplash.com/photo-1604277228829-1dde737d9096?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxsYXRlJTIwbmlnaHQlMjBmb29kfGVufDF8fHx8MTc2MzY3NzY2NHww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'all-day', label: 'Any time!', image: 'https://images.unsplash.com/photo-1761245193924-53a5a4bed9ef?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjbGFzc2ljJTIwYW1lcmljYW4lMjBkaW5lcnxlbnwxfHx8fDE3NjM2Nzc2NjF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'special-occasion', label: 'Special occasions', image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmaW5lJTIwZGluaW5nJTIwcmVzdGF1cmFudHxlbnwxfHx8fDE3NjM1NzU1ODd8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
    ],
  },
  {
    id: 'dish-type',
    title: 'What type of dish sounds best right now?',
    options: [
      { id: 'bowl', label: 'Bowl', image: 'https://images.unsplash.com/photo-1628521061262-19b5cdb7eee5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxyaWNlJTIwYm93bHxlbnwxfHx8fDE3NjM2NzQ0MzV8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'sandwich', label: 'Sandwich/Wrap', image: 'https://images.unsplash.com/photo-1666819604716-7b60a604bb76?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzYW5kd2ljaCUyMGRlbGl8ZW58MXx8fHwxNzYzNjM1MjE2fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'salad', label: 'Salad', image: 'https://images.unsplash.com/photo-1620019989479-d52fcedd99fe?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmcmVzaCUyMHNhbGFkJTIwYm93bHxlbnwxfHx8fDE3NjM2NjcwNDd8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'soup', label: 'Soup', image: 'https://images.unsplash.com/photo-1703322429243-05d349bc5c83?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzb3VwJTIwYnJlYWR8ZW58MXx8fHwxNzYzNjc3NjY1fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'burger-fries', label: 'Burger & fries', image: 'https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxidXJnZXIlMjBmcmllc3xlbnwxfHx8fDE3NjM2NTU1MTF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'pizza', label: 'Pizza', image: 'https://images.unsplash.com/photo-1544982503-9f984c14501a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwaXp6YSUyMHNsaWNlfGVufDF8fHx8MTc2MzY0NjY0M3ww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
    ],
  },
  {
    id: 'service',
    title: 'How do you prefer to order?',
    options: [
      { id: 'table-service', label: 'Full table service', image: 'https://images.unsplash.com/photo-1613274554329-70f997f5789f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxyZXN0YXVyYW50JTIwaW50ZXJpb3IlMjBtb2Rlcm58ZW58MXx8fHwxNzYzNjI0MzIzfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'counter', label: 'Counter/quick service', image: 'https://images.unsplash.com/photo-1762015669851-4098e655ec87?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmYXN0JTIwZm9vZCUyMGNvdW50ZXJ8ZW58MXx8fHwxNzYzNjM3NTk5fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'buffet', label: 'Buffet/Self-serve', image: 'https://images.unsplash.com/photo-1729708475294-fb3be3809dcb?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxidWZmZXQlMjBzcHJlYWR8ZW58MXx8fHwxNzYzNjc3NjY5fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'food-truck', label: 'Food truck', image: 'https://images.unsplash.com/photo-1574028742226-ee1ab3520a7f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmb29kJTIwdHJ1Y2slMjBzdHJlZXR8ZW58MXx8fHwxNzYzNjMwNjQxfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'patio', label: 'Outdoor patio', image: 'https://images.unsplash.com/photo-1697378006953-40c5bb9e6ca5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxyZXN0YXVyYW50JTIwcGF0aW8lMjBvdXRkb29yfGVufDF8fHx8MTc2MzY3NzY2OHww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'bar-seating', label: 'Bar seating', image: 'https://images.unsplash.com/photo-1598994671512-395d7a6147e0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb2NrdGFpbCUyMGJhcnxlbnwxfHx8fDE3NjM1NzczMDF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
    ],
  },
  {
    id: 'sides',
    title: 'Pick your ideal side dish!',
    options: [
      { id: 'fries', label: 'Fries', image: 'https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxidXJnZXIlMjBmcmllc3xlbnwxfHx8fDE3NjM2NTU1MTF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'rice', label: 'Rice', image: 'https://images.unsplash.com/photo-1628521061262-19b5cdb7eee5?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxyaWNlJTIwYm93bHxlbnwxfHx8fDE3NjM2NzQ0MzV8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'veggies', label: 'Grilled veggies', image: 'https://images.unsplash.com/photo-1625944227313-4f7f68e6b3fa?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxncmlsbGVkJTIwdmVnZXRhYmxlc3xlbnwxfHx8fDE3NjM2MjkwMDR8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'salad', label: 'Side salad', image: 'https://images.unsplash.com/photo-1620019989479-d52fcedd99fe?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmcmVzaCUyMHNhbGFkJTIwYm93bHxlbnwxfHx8fDE3NjM2NjcwNDd8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'soup', label: 'Soup', image: 'https://images.unsplash.com/photo-1703322429243-05d349bc5c83?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzb3VwJTIwYnJlYWR8ZW58MXx8fHwxNzYzNjc3NjY1fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'wings', label: 'Wings', image: 'https://images.unsplash.com/photo-1567620832903-9fc6debc209f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjaGlja2VuJTIwd2luZ3N8ZW58MXx8fHwxNzYzNjc0NzMyfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
    ],
  },
  {
    id: 'dessert',
    title: 'Finally, how are you ending your meal?',
    options: [
      { id: 'cake', label: 'Cake', image: 'https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjaG9jb2xhdGUlMjBjYWtlfGVufDF8fHx8MTc2MzYxNDc5NXww&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'ice-cream', label: 'Ice cream', image: 'https://images.unsplash.com/photo-1559703248-dcaaec9fab78?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxpY2UlMjBjcmVhbSUyMGNvbmV8ZW58MXx8fHwxNzYzNjM4NzIyfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'tiramisu', label: 'Tiramisu', image: 'https://images.unsplash.com/photo-1714385905983-6f8e06fffae1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0aXJhbWlzdSUyMGRlc3NlcnR8ZW58MXx8fHwxNzYzNjMyNjIxfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'creme-brulee', label: 'Crème brûlée', image: 'https://images.unsplash.com/photo-1676300184943-09b2a08319a3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjcmVtZSUyMGJydWxlZXxlbnwxfHx8fDE3NjM2NzU0NDJ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'fruit', label: 'Fresh fruit', image: 'https://images.unsplash.com/photo-1574198998217-deedebc22a4a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmcmVzaCUyMGZydWl0JTIwZGVzc2VydHxlbnwxfHx8fDE3NjM2Nzc2Njd8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
      { id: 'no-dessert', label: "I'll skip it", image: 'https://images.unsplash.com/photo-1585494156145-1c60a4fe952b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb2ZmZWUlMjBsYXR0ZXxlbnwxfHx8fDE3NjM2MDk3NzF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral' },
    ],
  },
];

export function BuzzfeedQuiz() {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [showDashboard, setShowDashboard] = useState(true); // Changed to true to show dashboard by default

  const handleOptionClick = (questionId: string, optionId: string) => {
    setAnswers((prev) => ({ ...prev, [questionId]: optionId }));
  };

  const handleSubmit = () => {
    if (Object.keys(answers).length === quizData.length) {
      setShowDashboard(true);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const allAnswered = Object.keys(answers).length === quizData.length;

  if (showDashboard) {
    return <Dashboard answers={answers} onRetake={() => { setAnswers({}); setShowDashboard(false); }} />;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="text-center mb-12">
        <h1 className="text-5xl mb-4">Find Your Restaurant Twin!</h1>
        <p className="text-xl text-slate-600">
          Answer 10 questions and we'll match you with your dining twin based on Yelp reviews
        </p>
      </div>

      <div className="space-y-16">
        {quizData.map((question) => (
          <div key={question.id} className="space-y-6">
            <div className="bg-[#6D3F1F] text-white px-8 py-12 rounded-lg text-center">
              <h2 className="text-3xl">{question.title}</h2>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {question.options.map((option) => (
                <button
                  key={option.id}
                  onClick={() => handleOptionClick(question.id, option.id)}
                  className={`group relative overflow-hidden rounded-lg transition-all ${
                    answers[question.id] === option.id
                      ? 'ring-4 ring-blue-500 scale-[0.98]'
                      : 'hover:scale-[1.02]'
                  }`}
                >
                  <div className="aspect-square">
                    <ImageWithFallback
                      src={option.image}
                      alt={option.label}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
                  <div className="absolute bottom-0 left-0 right-0 p-4 text-white text-center">
                    <p className="text-lg drop-shadow-lg">{option.label}</p>
                  </div>
                  {answers[question.id] === option.id && (
                    <div className="absolute top-2 right-2 bg-blue-500 text-white rounded-full w-8 h-8 flex items-center justify-center">
                      ✓
                    </div>
                  )}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="sticky bottom-0 bg-white border-t border-slate-200 py-6 mt-12 -mx-4 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <Button
            onClick={handleSubmit}
            disabled={!allAnswered}
            size="lg"
            className="w-full md:w-auto px-12"
          >
            {allAnswered ? 'See Your Results!' : `Answer All Questions (${Object.keys(answers).length}/${quizData.length})`}
          </Button>
        </div>
      </div>
    </div>
  );
}
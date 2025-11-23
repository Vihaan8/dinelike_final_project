import { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { RadioGroup, RadioGroupItem } from './ui/radio-group';
import { Label } from './ui/label';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Progress } from './ui/progress';
import { CheckCircle2 } from 'lucide-react';

interface Question {
  id: string;
  type: 'text' | 'radio' | 'textarea';
  question: string;
  options?: string[];
}

const questions: Question[] = [
  {
    id: 'name',
    type: 'text',
    question: 'What is your name?',
  },
  {
    id: 'experience',
    type: 'radio',
    question: 'How would you describe your experience level?',
    options: ['Beginner', 'Intermediate', 'Advanced', 'Expert'],
  },
  {
    id: 'preference',
    type: 'radio',
    question: 'Which do you prefer?',
    options: ['Option A', 'Option B', 'Option C', 'Option D'],
  },
  {
    id: 'feedback',
    type: 'textarea',
    question: 'Please share any additional comments or feedback:',
  },
];

export function Questionnaire() {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [isComplete, setIsComplete] = useState(false);

  const currentQuestion = questions[currentStep];
  const progress = ((currentStep + 1) / questions.length) * 100;

  const handleAnswer = (value: string) => {
    setAnswers({ ...answers, [currentQuestion.id]: value });
  };

  const handleNext = () => {
    if (currentStep < questions.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      setIsComplete(true);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleRestart = () => {
    setCurrentStep(0);
    setAnswers({});
    setIsComplete(false);
  };

  const canProceed = answers[currentQuestion?.id];

  if (isComplete) {
    return (
      <div className="max-w-2xl mx-auto">
        <Card className="shadow-lg">
          <CardHeader className="text-center">
            <div className="flex justify-center mb-4">
              <CheckCircle2 className="w-16 h-16 text-green-500" />
            </div>
            <CardTitle>Thank You!</CardTitle>
            <CardDescription>Your responses have been recorded</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-slate-50 rounded-lg p-6 space-y-3">
              {questions.map((question) => (
                <div key={question.id} className="border-b border-slate-200 pb-3 last:border-0">
                  <p className="text-slate-600 text-sm">{question.question}</p>
                  <p className="mt-1">{answers[question.id]}</p>
                </div>
              ))}
            </div>
          </CardContent>
          <CardFooter className="flex justify-center">
            <Button onClick={handleRestart}>Start Over</Button>
          </CardFooter>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <Card className="shadow-lg">
        <CardHeader>
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-slate-600">
              Question {currentStep + 1} of {questions.length}
            </span>
          </div>
          <Progress value={progress} className="mb-4" />
          <CardTitle>{currentQuestion.question}</CardTitle>
        </CardHeader>
        <CardContent>
          {currentQuestion.type === 'text' && (
            <Input
              placeholder="Type your answer here..."
              value={answers[currentQuestion.id] || ''}
              onChange={(e) => handleAnswer(e.target.value)}
            />
          )}

          {currentQuestion.type === 'radio' && currentQuestion.options && (
            <RadioGroup
              value={answers[currentQuestion.id] || ''}
              onValueChange={handleAnswer}
            >
              <div className="space-y-3">
                {currentQuestion.options.map((option) => (
                  <div
                    key={option}
                    className="flex items-center space-x-3 border rounded-lg p-4 hover:bg-slate-50 transition-colors cursor-pointer"
                  >
                    <RadioGroupItem value={option} id={option} />
                    <Label htmlFor={option} className="flex-1 cursor-pointer">
                      {option}
                    </Label>
                  </div>
                ))}
              </div>
            </RadioGroup>
          )}

          {currentQuestion.type === 'textarea' && (
            <Textarea
              placeholder="Type your answer here..."
              value={answers[currentQuestion.id] || ''}
              onChange={(e) => handleAnswer(e.target.value)}
              rows={6}
            />
          )}
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button
            variant="outline"
            onClick={handlePrevious}
            disabled={currentStep === 0}
          >
            Previous
          </Button>
          <Button onClick={handleNext} disabled={!canProceed}>
            {currentStep === questions.length - 1 ? 'Submit' : 'Next'}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}

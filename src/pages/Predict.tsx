import { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { MedicalSwitch } from '@/components/ui/medical-switch';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { AlertCircle, CheckCircle, Activity, TrendingUp, Loader2 } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/contexts/AuthContext';
import { NavLink } from 'react-router-dom';

const API_URL = "http://127.0.0.1:5000";

interface FormData {
  polyuria: boolean;
  polydipsia: boolean;
  suddenWeightLoss: boolean;
  partialParesis: boolean;
  visualBlurring: boolean;
  alopecia: boolean;
  irritability: boolean;
  gender: 'Male' | 'Female' | '';
}

interface PredictionResult {
  prediction: 'Diabetic' | 'Non-Diabetic';
  confidence: number;
  riskFactors: string[];
  recommendations: string[];
}

const Predict = () => {
  const { user } = useAuth();
  const { toast } = useToast();
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [formData, setFormData] = useState<FormData>({
    polyuria: false,
    polydipsia: false,
    suddenWeightLoss: false,
    partialParesis: false,
    visualBlurring: false,
    alopecia: false,
    irritability: false,
    gender: '',
  });
const medicalQuestions = [
  { key: 'polyuria' as keyof FormData, label: 'Polyuria', description: 'Frequent urination, especially at night' },
  { key: 'polydipsia' as keyof FormData, label: 'Polydipsia', description: 'Excessive thirst' },
  { key: 'suddenWeightLoss' as keyof FormData, label: 'Sudden Weight Loss', description: 'Unexplained weight loss' },
  { key: 'partialParesis' as keyof FormData, label: 'Partial Paresis', description: 'Weakness in limbs' },
  { key: 'visualBlurring' as keyof FormData, label: 'Visual Blurring', description: 'Blurred vision' },
  { key: 'alopecia' as keyof FormData, label: 'Alopecia', description: 'Hair loss' },
  { key: 'irritability' as keyof FormData, label: 'Irritability', description: 'Mood changes' },
];
const updateFormData = <K extends keyof FormData>(
  key: K,
  value: FormData[K]
) => {
  setFormData(prev => ({ ...prev, [key]: value }));
};
  useEffect(() => {
    axios.get(API_URL).catch(() => {});
  }, []);

  const callBackendPredict = async (data: FormData): Promise<PredictionResult> => {

    const res = await axios.post(`${API_URL}/predict`, data);
    return res.data;

  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!user) {
      toast({ title: "Login required", variant: "destructive" });
      return;
    }

    setIsLoading(true);

    try {
      const prediction = await callBackendPredict(formData);
      setResult(prediction);
    } catch (err) {
      toast({ title: "Prediction failed", variant: "destructive" });
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      polyuria: false,
      polydipsia: false,
      suddenWeightLoss: false,
      partialParesis: false,
      visualBlurring: false,
      alopecia: false,
      irritability: false,
      gender: '',
    });
    setResult(null);
  };


  // ⭐ YOUR UI BELOW REMAINS EXACTLY SAME
  if (!user) {
    return (
      <div className="min-h-screen bg-background py-12 px-4">
        <div className="max-w-2xl mx-auto text-center">
          <div className="medical-card p-8">
            <AlertCircle className="h-16 w-16 text-medical-warning mx-auto mb-4" />
            <h1 className="text-2xl font-bold mb-4">Authentication Required</h1>
            <p className="text-muted-foreground mb-6">
              Please log in to access the diabetes prediction tool and keep track of your assessments.
            </p>
            <NavLink to="/login">
              <Button className="bg-gradient-primary">Go to Login</Button>
            </NavLink>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold mb-4">Diabetes Risk Assessment</h1>
          <p className="text-xl text-muted-foreground">
            Answer the questions below to get your personalized risk evaluation
          </p>
        </div>

        {result ? (
          <div className="space-y-6 animate-fade-in">
            <Card className="medical-card shadow-medical-strong">
              <CardHeader className="text-center">
                <div className={`w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4 ${
                  result.prediction === 'Diabetic' ? 'bg-medical-danger text-white' : 'bg-medical-success text-white'
                }`}>
                  {result.prediction === 'Diabetic' ? <AlertCircle className="h-10 w-10" /> : <CheckCircle className="h-10 w-10" />}
                </div>
                <CardTitle className="text-2xl">Prediction: {result.prediction}</CardTitle>
                <CardDescription>Confidence: {(result.confidence).toFixed(1)}%</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {result.riskFactors.length > 0 && (
                  <div>
                    <h3 className="font-semibold mb-3 flex items-center">
                      <TrendingUp className="h-4 w-4 mr-2" /> Identified Risk Factors
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {result.riskFactors.map((factor, index) => (
                        <Badge key={index} variant="outline" className="border-medical-warning">{factor}</Badge>
                      ))}
                    </div>
                  </div>
                )}

                <div>
                  <h3 className="font-semibold mb-3 flex items-center">
                    <Activity className="h-4 w-4 mr-2" /> Recommendations
                  </h3>
                  <ul className="space-y-2">
                    {result.recommendations.map((rec, index) => (
                      <li key={index} className="flex items-start gap-2 text-sm">
                        <CheckCircle className="h-4 w-4 text-medical-success mt-0.5 flex-shrink-0" />
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="bg-muted/50 p-4 rounded-lg">
                  <p className="text-sm text-muted-foreground">
                    <strong>Important:</strong> This assessment is for educational purposes only and should not replace professional medical advice.
                  </p>
                </div>

                <Button onClick={resetForm} variant="outline" className="w-full">
                  Take Another Assessment
                </Button>
              </CardContent>
            </Card>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-6">
            <Card className="medical-card">
              <CardHeader>
                <CardTitle>Gender</CardTitle>
                <CardDescription>Please select your gender</CardDescription>
              </CardHeader>
              <CardContent>
                <RadioGroup
                  value={formData.gender}
                  onValueChange={(value: 'Male' | 'Female') => updateFormData('gender', value)}
                >
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="Male" id="male" />
                    <Label htmlFor="male">Male</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="Female" id="female" />
                    <Label htmlFor="female">Female</Label>
                  </div>
                </RadioGroup>
              </CardContent>
            </Card>

            <Card className="medical-card">
              <CardHeader>
                <CardTitle>Symptom Assessment</CardTitle>
                <CardDescription>Please indicate if you are currently experiencing any of these symptoms</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                {medicalQuestions.map((question) => (
                  <MedicalSwitch
                    key={question.key}
                    id={question.key}
                    label={question.label}
                    description={question.description}
                    value={formData[question.key] as boolean}
                    onChange={(value) => updateFormData(question.key, value)}
                  />
                ))}
              </CardContent>
            </Card>

            <Button
              type="submit"
              className="w-full bg-gradient-primary shadow-medical-medium"
              size="lg"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Analyzing...
                </>
              ) : 'Get Diabetes Risk Assessment'}
            </Button>
          </form>
        )}
      </div>
    </div>
  );
};

export default Predict;

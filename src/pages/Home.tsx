import { NavLink } from 'react-router-dom';
import { Activity, Shield, Users, Zap, ArrowRight, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const Home = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-hero py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-white/10 text-white mb-8 animate-fade-in">
              <Activity className="h-4 w-4 mr-2" />
              <span className="text-sm font-medium">Advanced AI-Powered Health Assessment</span>
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6 animate-slide-up">
              Diabetes Risk
              <br />
              <span className="text-white/90">Assessment Tool</span>
            </h1>
            
            <p className="text-xl text-white/80 mb-8 max-w-3xl mx-auto animate-slide-up">
              Get personalized diabetes risk assessment using advanced machine learning. 
              Quick, accurate, and designed by medical professionals.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center animate-slide-up">
              <NavLink to="/predict">
                <Button size="lg" className="bg-white text-primary hover:bg-white/90 shadow-medical-medium">
                  Start Assessment
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </NavLink>
              <Button variant="outline" size="lg" className="border-white text-white hover:bg-white/10">
                Learn More
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Why Choose Our Assessment Tool?
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Combining medical expertise with cutting-edge AI to provide you with reliable health insights.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="medical-card text-center group hover:scale-105 transition-transform">
              <CardHeader>
                <div className="w-16 h-16 bg-gradient-primary rounded-full flex items-center justify-center mx-auto mb-4">
                  <Zap className="h-8 w-8 text-white" />
                </div>
                <CardTitle>Instant Results</CardTitle>
                <CardDescription>
                  Get your risk assessment in seconds with our advanced AI model
                </CardDescription>
              </CardHeader>
            </Card>
            
            <Card className="medical-card text-center group hover:scale-105 transition-transform">
              <CardHeader>
                <div className="w-16 h-16 bg-gradient-primary rounded-full flex items-center justify-center mx-auto mb-4">
                  <Shield className="h-8 w-8 text-white" />
                </div>
                <CardTitle>Medical Grade</CardTitle>
                <CardDescription>
                  Trained on medical data and validated by healthcare professionals
                </CardDescription>
              </CardHeader>
            </Card>
            
            <Card className="medical-card text-center group hover:scale-105 transition-transform">
              <CardHeader>
                <div className="w-16 h-16 bg-gradient-primary rounded-full flex items-center justify-center mx-auto mb-4">
                  <Users className="h-8 w-8 text-white" />
                </div>
                <CardTitle>Privacy First</CardTitle>
                <CardDescription>
                  Your health data is processed securely and never stored permanently
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-4 bg-muted/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              How It Works
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Simple steps to get your personalized diabetes risk assessment
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-primary text-primary-foreground rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                1
              </div>
              <h3 className="font-semibold mb-2">Answer Questions</h3>
              <p className="text-sm text-muted-foreground">
                Complete our quick health questionnaire about symptoms and demographics
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-primary text-primary-foreground rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                2
              </div>
              <h3 className="font-semibold mb-2">AI Analysis</h3>
              <p className="text-sm text-muted-foreground">
                Our trained model analyzes your responses using medical patterns
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-primary text-primary-foreground rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                3
              </div>
              <h3 className="font-semibold mb-2">Get Results</h3>
              <p className="text-sm text-muted-foreground">
                Receive your personalized risk assessment with explanations
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 bg-primary text-primary-foreground rounded-full flex items-center justify-center mx-auto mb-4 text-xl font-bold">
                4
              </div>
              <h3 className="font-semibold mb-2">Take Action</h3>
              <p className="text-sm text-muted-foreground">
                Get personalized recommendations and consult with healthcare providers
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Check Your Diabetes Risk?
          </h2>
          <p className="text-xl text-muted-foreground mb-8">
            Take the first step towards better health with our AI-powered assessment tool.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <NavLink to="/predict">
              <Button size="lg" className="bg-gradient-primary shadow-medical-medium">
                Start Your Assessment
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </NavLink>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-12 pt-8 border-t border-border">
            <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
              <CheckCircle className="h-4 w-4 text-medical-success" />
              <span>Takes less than 2 minutes</span>
            </div>
            <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
              <CheckCircle className="h-4 w-4 text-medical-success" />
              <span>No personal data stored</span>
            </div>
            <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
              <CheckCircle className="h-4 w-4 text-medical-success" />
              <span>Medically validated</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
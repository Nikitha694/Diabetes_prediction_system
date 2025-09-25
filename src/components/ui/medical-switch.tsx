import { useState } from 'react';
import { cn } from '@/lib/utils';

interface MedicalSwitchProps {
  id: string;
  label: string;
  description?: string;
  value: boolean;
  onChange: (value: boolean) => void;
  disabled?: boolean;
}

export const MedicalSwitch = ({
  id,
  label,
  description,
  value,
  onChange,
  disabled = false,
}: MedicalSwitchProps) => {
  return (
    <div className="flex items-center justify-between p-4 medical-card hover:shadow-medical-medium transition-all">
      <div className="flex-1">
        <label
          htmlFor={id}
          className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
        >
          {label}
        </label>
        {description && (
          <p className="text-xs text-muted-foreground mt-1">{description}</p>
        )}
      </div>
      
      <button
        type="button"
        role="switch"
        aria-checked={value}
        disabled={disabled}
        onClick={() => !disabled && onChange(!value)}
        className={cn(
          'medical-switch-track focus-visible:ring-offset-2',
          value
            ? 'bg-primary'
            : 'bg-input',
          disabled && 'opacity-50 cursor-not-allowed'
        )}
      >
        <span
          className={cn(
            'medical-switch-thumb',
            value ? 'translate-x-5' : 'translate-x-0'
          )}
        />
      </button>
    </div>
  );
};
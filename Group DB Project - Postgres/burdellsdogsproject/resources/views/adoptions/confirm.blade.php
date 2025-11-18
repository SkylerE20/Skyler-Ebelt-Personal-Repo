<!DOCTYPE html>
<html>
<head>
    <title>Confirm Adoption</title>
    <style>
    </style>
</head>
<body>
    <h1>Confirm Adoption</h1>
    
    @if ($errors->any())
        <div class="alert">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif
    
    <div class="container">
        <div class="info-box">
            <h2>Applicant Information</h2>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">Name:</span> 
                    {{ $applicant->first_name }} {{ $applicant->last_name }}
                </div>
                <div class="info-item">
                    <span class="info-label">Email:</span> 
                    {{ $applicant->applicant_email }}
                </div>
                <div class="info-item">
                    <span class="info-label">Phone:</span> 
                    {{ $applicant->applicant_phone }}
                </div>
                <div class="info-item">
                    <span class="info-label">Address:</span> 
                    {{ $applicant->street }}, {{ $applicant->city }}, {{ $applicant->state_abbrev }} {{ $applicant->zip_code }}
                </div>
                <div class="info-item">
                    <span class="info-label">Household Size:</span> 
                    {{ $applicant->household_size }}
                </div>
                <div class="info-item">
                    <span class="info-label">Application Date:</span> 
                    {{ $applicant->application_date }}
                </div>
            </div>
        </div>
        
        <div class="info-box">
            <h2>Dog Information</h2>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">ID:</span> 
                    {{ $dog->dog_id }}
                </div>
                <div class="info-item">
                    <span class="info-label">Name:</span> 
                    {{ $dog->dog_name }}
                </div>
                <div class="info-item">
                    <span class="info-label">Breed(s):</span> 
                    {{ $dog->breeds ?: 'Unknown' }}
                </div>
                <div class="info-item">
                    <span class="info-label">Sex:</span> 
                    {{ $dog->sex }}
                </div>
                <div class="info-item">
                    <span class="info-label">Age:</span> 
                    {{ $dog->age }}
                </div>
                <div class="info-item">
                    <span class="info-label">Altered:</span> 
                    {{ $dog->altered ? 'Yes' : 'No' }}
                </div>
                <div class="info-item">
                    <span class="info-label">From Animal Control:</span> 
                    {{ $dog->surrendered_by_animal_control ? 'Yes' : 'No' }}
                </div>
                <div class="info-item">
                    <span class="info-label">Surrender Date:</span> 
                    {{ $dog->surrender_date }}
                </div>
                <div class="info-item">
                    <span class="info-label">Total Expenses:</span> 
                    ${{ number_format($totalExpenses, 2) }}
                </div>
            </div>
        </div>
    </div>
    
    <div class="adoption-form">
    <h2>Adoption Details</h2>
    
    <div class="fee-display">
        Adoption Fee: ${{ is_numeric($adoptionFee) ? number_format($adoptionFee, 2) : $adoptionFee }}
    </div>
    
    <a href="{{ url('/dogdashboard') }}" class="back-link">Back to Dashboard</a>
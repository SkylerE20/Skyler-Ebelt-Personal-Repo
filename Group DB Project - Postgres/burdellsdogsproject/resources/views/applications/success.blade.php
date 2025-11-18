<!DOCTYPE html>
<html>
<head>
    <title>Application Submitted</title>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Application Submitted</h2>
        </div>

        <div class="text-center">
            <div class="success-message">
                <h3>Thank You!</h3>
                <p>Your adoption application has been successfully submitted.</p>
            </div>
            
            <p><strong>Application Details:</strong></p>
            <p>Email: {{ $email }}</p>
            <p>Date Submitted: {{ date('F j, Y', strtotime($date)) }}</p>
            
            @if(isset($dog))
            <div class="dog-details">
                <h4>Dog Selected for Adoption:</h4>
                <div class="dog-title">{{ $dog->dog_name }} (ID: {{ $dog->dog_id }})</div>
                <p>{{ $dog->breeds }}, {{ $dog->sex }}, {{ $dog->age }} years old</p>
            </div>
            @endif
            <a href="{{ url('/dogdashboard') }}" class="button">Return to Dashboard</a>
        </div>
    </div>
</body>
</html>
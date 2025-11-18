<html>
<head>
    <title>Review Application</title>
</head>
<style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        padding: 5px;
    }
</style>
<body>
    <h1>Review Application</h1>
    
    @if (session('success'))
        <div class="success-message">
            {{ session('success') }}
        </div>
    @endif
    
    @if ($errors->any())
        <div class="error-message">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif
    
    <div class="application-details">
        <h2>Applicant Information</h2>
        <div class="detail-grid">
            <div class="detail-item">
                <span class="detail-label">Name:</span> 
                {{ $application->first_name }} {{ $application->last_name }}
            </div>
            <div class="detail-item">
                <span class="detail-label">Email:</span> 
                {{ $application->applicant_email }}
            </div>
            <div class="detail-item">
                <span class="detail-label">Phone:</span> 
                {{ $application->applicant_phone }}
            </div>
            <div class="detail-item">
                <span class="detail-label">Household Size:</span> 
                {{ $application->household_size }}
            </div>
            <div class="detail-item">
                <span class="detail-label">Address:</span> 
                {{ $application->street }}, {{ $application->city }}, 
                {{ $application->state_abbrev }} {{ $application->zip_code }}
            </div>
            <div class="detail-item">
                <span class="detail-label">Application Date:</span> 
                {{ date('m/d/Y', strtotime($application->application_date)) }}
            </div>
            <div class="detail-item">
                <span class="detail-label">Status:</span> 
                <span class="status-{{ strtolower($application->status) }}">{{ $application->status }}</span>
                @if ($application->status === 'Approved')
                    <br>Approved on: {{ date('m/d/Y', strtotime($application->accept_date)) }}
                @elseif ($application->status === 'Rejected')
                    <br>Rejected on: {{ date('m/d/Y', strtotime($application->reject_date)) }}
                @endif
            </div>
        </div>
        
        <h2>Selected Dog</h2>
        @if(isset($relatedDogs) && is_countable($relatedDogs) && count($relatedDogs) > 0)
            <div class="dog-details">
                @foreach($relatedDogs as $dog)
                    <div class="dog-card">
                        <h3>{{ $dog->dog_name }} (ID: {{ $dog->dog_id }})</h3>
                        <div class="dog-info">
                            @if(isset($dog->breeds))
                                <p><strong>Breed(s):</strong> {{ $dog->breeds }}</p>
                            @endif
                            <p><strong>Sex:</strong> {{ $dog->sex }}</p>
                            <p><strong>Age:</strong> {{ $dog->age }} years old</p>
                            <p><strong>Description:</strong> {{ $dog->description }}</p>
                            @if($application->status === 'Approved' && isset($dog->actual_adoption_date))
                                <p><strong>Adoption Date:</strong> {{ date('m/d/Y', strtotime($dog->actual_adoption_date)) }}</p>
                                <p><strong>Adoption Fee:</strong> ${{ number_format($dog->fee, 2) }}</p>
                            @endif
                        </div>
                    </div>
                @endforeach
            </div>
        @else
            <p class="info-message">No dog information available for this application.</p>
        @endif
        
        @if($application->status === 'Pending')
            <div class="action-buttons">
                <form action="{{ route('applications.approve', ['email' => $application->applicant_email, 'date' => $application->application_date]) }}" method="POST" style="display: inline;">
                    @csrf
                    <button type="submit" class="approve-button">Approve Application</button>
                </form>
                
                <form action="{{ route('applications.reject', ['email' => $application->applicant_email, 'date' => $application->application_date]) }}" method="POST" style="display: inline;">
                    @csrf
                    <button type="submit" class="reject-button">Reject Application</button>
                </form>
            </div>
        @endif
    </div>
    
    <a href="{{ route('applications.index') }}" class="back-link">Back to Applications</a>
</body>
</html>
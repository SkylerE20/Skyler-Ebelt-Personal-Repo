<!DOCTYPE html>
<html>
<head>
    <title>Select Dog for Adoption</title>
</head>
<body>
    <h1>Select a Dog for Adoption</h1>
    
    @if ($errors->any())
        <div class="alert">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif
    
    <div class="applicant-info">
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
            <div class="info-item">
                <span class="info-label">Approval Date:</span> 
                {{ $applicant->accept_date }}
            </div>
        </div>
    </div>
    
    <h2>Available Dogs</h2>
    
    @if(count($dogs) > 0)
        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Breed(s)</th>
                <th>Sex</th>
                <th>Age</th>
                <th>Altered</th>
                <th>From Animal Control</th>
                <th>Surrender Date</th>
                <th>Action</th>
            </tr>
            
            @foreach($dogs as $dog)
                <tr>
                    <td>{{ $dog->dog_id }}</td>
                    <td>{{ $dog->dog_name }}</td>
                    <td>{{ $dog->breeds ?: 'Unknown' }}</td>
                    <td>{{ $dog->sex }}</td>
                    <td>{{ $dog->age }}</td>
                    <td>{{ $dog->altered ? 'Yes' : 'No' }}</td>
                    <td>{{ $dog->surrendered_by_animal_control ? 'Yes' : 'No' }}</td>
                    <td>{{ $dog->surrender_date }}</td>
                    <td>
                        <a href="{{ route('adoptions.confirm', ['email' => $applicant->applicant_email, 'date' => $applicant->application_date, 'dogId' => $dog->dog_id]) }}" class="action-link">
                            Select
                        </a>
                    </td>
                </tr>
            @endforeach
        </table>
    @else
        <div class="no-dogs">
            <p>No available dogs found for adoption.</p>
        </div>
    @endif
    
    <a href="{{ route('adoptions.index') }}" class="back-link">Back to Search</a>
</body>
</html>
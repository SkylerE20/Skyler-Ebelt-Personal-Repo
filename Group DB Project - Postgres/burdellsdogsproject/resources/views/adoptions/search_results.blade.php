<!DOCTYPE html>
<html>
<head>
    <title>Search Results - Adoption Applications</title>
</head>
<body>
    <h1>Search Results - Approved Adoption Applications</h1>
    
    @if(count($applications) > 0)
        <table>
            <tr>
                <th>Name</th>
                <th>Phone</th>
                <th>Address</th>
                <th>Household Size</th>
                <th>Application Date</th>
                <th>Approved Date</th>
                <th>Action</th>
            </tr>
            
            @foreach($applications as $application)
                <tr>
                    <td>{{ $application->first_name }} {{ $application->last_name }}</td>
                    <td>{{ $application->applicant_phone }}</td>
                    <td>
                        {{ $application->street }}, {{ $application->city }}, 
                        {{ $application->state_abbrev }} {{ $application->zip_code }}
                    </td>
                    <td>{{ $application->household_size }}</td>
                    <td>{{ $application->application_date }}</td>
                    <td>{{ $application->accept_date }}</td>
                    <td>
                        <a href="{{ route('adoptions.select_dog', ['email' => $application->applicant_email, 'date' => $application->application_date]) }}" class="action-link">
                            Select for Adoption
                        </a>
                    </td>
                </tr>
            @endforeach
        </table>
    @else
        <div class="no-results">
            <p>No approved adoption applications found matching your search criteria.</p>
        </div>
    @endif
    
    <a href="{{ route('adoptions.index') }}" class="back-link">Back to Search</a>
</body>
</html>
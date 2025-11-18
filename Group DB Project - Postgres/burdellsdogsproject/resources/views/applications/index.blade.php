<!DOCTYPE html>
<html>
<head>
    <title>Adoption Applications</title>
</head>
<style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        padding: 5px;
    }
</style>
<body>
    <h1>Adoption Applications</h1>
    
    @if (session('success'))
        <div class="success-message">
            {{ session('success') }}
        </div>
    @endif

    @if ($errors->any())
        <div class="error-list">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif
    
    <div class="search-form">
        <form action="{{ route('applications.index') }}" method="GET">
            <div class="form-group">
                <label for="search_last_name">Last Name:</label>
                <input type="text" id="search_last_name" name="search_last_name" value="{{ $searchLastName ?? '' }}" placeholder="Search by last name">
            </div>
            
            <div class="form-group">
                <label for="status">Status:</label>
                <select id="status" name="status">
                    <option value="all" {{ ($searchStatus ?? 'all') == 'all' ? 'selected' : '' }}>All</option>
                    <option value="approved" {{ ($searchStatus ?? '') == 'approved' ? 'selected' : '' }}>Approved</option>
                    <option value="rejected" {{ ($searchStatus ?? '') == 'rejected' ? 'selected' : '' }}>Rejected</option>
                    <option value="pending" {{ ($searchStatus ?? '') == 'pending' ? 'selected' : '' }}>Pending</option>
                </select>
            </div>
            
            <button type="submit">Search</button>
        </form>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Applicant</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Household Size</th>
                <th>Dog</th>
                <th>Application Date</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            @if(count($applications) > 0)
                @foreach($applications as $app)
                <tr>
                    <td>{{ $app->first_name }} {{ $app->last_name }}</td>
                    <td>{{ $app->applicant_email }}</td>
                    <td>{{ $app->applicant_phone }}</td>
                    <td>{{ $app->household_size }}</td>
                    <td>
                        @if(isset($app->dog_name))
                            {{ $app->dog_name }} 
                            <div class="dog-id">ID: {{ $app->dog_id }}</div>
                        @else
                            <span class="text-danger">No dog selected</span>
                        @endif
                    </td>
                    <td>{{ date('m/d/Y', strtotime($app->application_date)) }}</td>
                    <td>
                        <span class="status-{{ strtolower($app->status) }}">{{ $app->status }}</span>
                        @if ($app->status === 'Approved')
                            <br>{{ date('m/d/Y', strtotime($app->accept_date)) }}
                        @elseif ($app->status === 'Rejected')
                            <br>{{ date('m/d/Y', strtotime($app->reject_date)) }}
                        @endif
                    </td>
                    <td>
                        <a href="{{ route('applications.review', ['email' => $app->applicant_email, 'date' => $app->application_date]) }}">
                            Review
                        </a>
                    </td>
                </tr>
                @endforeach
            @else
                <tr>
                    <td colspan="8" class="no-applications">No applications found</td>
                </tr>
            @endif
        </tbody>
    </table>
    
    <a href="{{ url('/dogdashboard') }}" class="back-link">Back to Dashboard</a>
</body>
</html>
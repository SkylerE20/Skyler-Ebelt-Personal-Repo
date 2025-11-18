<!DOCTYPE html>
<html>
<head>
    <title>Adoption Form</title>
</head>
<body>
    <h1>Adoption Form</h1>
    
    @if ($errors->any())
        <div class="alert">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif
    
    <div class="search-form">
        <h2>Search Approved Adoption Applications</h2>
        <form action="{{ route('adoptions.search') }}" method="POST">
            @csrf
            <label for="last_name">Last Name:</label>
            <input type="text" id="last_name" name="last_name" placeholder="Enter last name to search" required>
            
            <button type="submit">Search</button>
        </form>
    </div>
    
    <a href="{{ url('/dogdashboard') }}" class="back-link">Back to Dashboard</a>
</body>
</html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Burdell's Dogs</title>
</head>
<style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        padding: 5px;
    }
</style>
<body>
    <h2>Volunteer Lookup Report</h2>
    <form action="/VolunteerLookup" method="POST">
        @csrf
        <input name="searchInput" type="text" placeholder="Name">
        <button>Search</button>
    </form>
    @if(isset($volunteerLookup))
        @if(count($volunteerLookup) > 0)
            <table>
                <tr>
                    <th>first_name</th>
                    <th>last_name</th>
                    <th>email_address</th>
                    <th>phone_number</th>
                </tr>
                @foreach ($volunteerLookup as $vol)
                <tr>
                    <td>{{ $vol->first_name }}</td>
                    <td>{{ $vol->last_name }}</td>
                    <td>{{ $vol->email_address }}</td>
                    <td>{{ $vol->phone_number }}</td>
                </tr>
                @endforeach
            </table>
        @else
            <p>No results found.</p>
        @endif
    @endif

</body>
</html>
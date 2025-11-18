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
    <h2>Volunteer Monthly Birthday Report</h2>
    
    <form id=searchForm action="/VolunteerBirthday" method="POST">

        @csrf
        @if($monthdd)
            <select name="monthdd">
                <option value="1" @if($monthdd == 1) selected @endif>January</option>
                <option value="2" @if($monthdd == 2) selected @endif>February</option>
                <option value="3" @if($monthdd == 3) selected @endif>March</option>
                <option value="4" @if($monthdd == 4) selected @endif>April</option>
                <option value="5" @if($monthdd == 5) selected @endif>May</option>
                <option value="6" @if($monthdd == 6) selected @endif>June</option>
                <option value="7" @if($monthdd == 7) selected @endif>July</option>
                <option value="8" @if($monthdd == 8) selected @endif>August</option>
                <option value="9" @if($monthdd == 9) selected @endif>September</option>
                <option value="10" @if($monthdd == 10) selected @endif>October</option>
                <option value="11" @if($monthdd == 11) selected @endif>November</option>
                <option value="12" @if($monthdd == 12) selected @endif>December</option>
            </select>
        @else
            <select name="monthdd">
                <option value="1" @if(date('n') == 1) selected @endif>January</option>
                <option value="2" @if(date('n') == 2) selected @endif>February</option>
                <option value="3" @if(date('n') == 3) selected @endif>March</option>
                <option value="4" @if(date('n') == 4) selected @endif>April</option>
                <option value="5" @if(date('n') == 5) selected @endif>May</option>
                <option value="6" @if(date('n') == 6) selected @endif>June</option>
                <option value="7" @if(date('n') == 7) selected @endif>July</option>
                <option value="8" @if(date('n') == 8) selected @endif>August</option>
                <option value="9" @if(date('n') == 9) selected @endif>September</option>
                <option value="10" @if(date('n') == 10) selected @endif>October</option>
                <option value="11" @if(date('n') == 11) selected @endif>November</option>
                <option value="12" @if(date('n') == 12) selected @endif>December</option>
            </select>
        @endif
        
        @if($yeardd)
            <select name="yeardd">
                <option value="0" @if($yeardd == 0) selected @endif>{{ date('Y') }}</option>
                <option value="1" @if($yeardd == 1) selected @endif>{{ date('Y') - 1 }}</option>
            </select>
        @else 
            <select name="yeardd">
                <option value="0" selected>{{ date('Y') }}</option>
                <option value="1">{{ date('Y') - 1 }}</option>
            </select>
        @endif
        
        <button>Search</button>
        
    </form>
    
    @if(!isset($volunteerBirthdayTable))
        <script>
            document.getElementById('searchForm').submit();
        </script>
    @endif

    @if(count($volunteerBirthdayTable) > 0)
        <table>
            <tr>
                <th>first_name</th>
                <th>last_name</th>
                <th>email_address</th>
                <th>milestone_birthday</th>
            </tr>
            @foreach ($volunteerBirthdayTable as $vol)
            <tr>
                <td>{{ $vol->first_name }}</td>
                <td>{{ $vol->last_name }}</td>
                <td>{{ $vol->email_address }}</td>
                <td>{{ $vol->milestone_birthday ? 'yes' : 'no'}}</td>
            </tr>
            @endforeach
        </table>
    @else
        <p>No birthdays found.</p>
    @endif
    
</body>
</html>
<!DOCTYPE html>
<html>
<head>
    <title>Dogs Adopted (60+ days) - {{ $month }}</title>
</head>
<style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        padding: 5px;
    }
</style>
<body>
    <h1>Dogs Adopted Who Spent 60+ Days at Rescue</h1>
    
    <table>
        <tr>
            <th>Dog ID</th>
            <th>Breed</th>
            <th>Sex</th>
            <th>Microchip ID</th>
            <th>Surrender Date</th>
            <th>Adoption Date</th>
            <th>Days in Rescue</th>
        </tr>
        
        @foreach($dogs as $dog)
            <tr>
                <td>{{ $dog->dog_id }}</td>
                <td>{{ $dog->breed }}</td>
                <td>{{ $dog->sex }}</td>
                <td>{{ $dog->microchip_id }}</td>
                <td>{{ $dog->surrender_date }}</td>
                <td>{{ $dog->adoption_date }}</td>
                <td>{{ $dog->days_in_rescue }}</td>
            </tr>
        @endforeach
    </table>
    
    <a href="{{ url('/reports/animal-control') }}" class="back-link">Back to Report</a>
</body>
</html>
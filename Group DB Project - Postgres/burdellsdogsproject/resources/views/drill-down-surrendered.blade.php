<!DOCTYPE html>
<html>
<head>
    <title>Animal Control Surrenders - {{ $month }}</title>
</head>
<style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        padding: 5px;
    }
</style>
<body>
    <h1>Animal Control Surrenders</h1>
    
    <table>
        <tr>
            <th>Dog ID</th>
            <th>Breed</th>
            <th>Sex</th>
            <th>Altered</th>
            <th>Microchip ID</th>
            <th>Surrender Date</th>
        </tr>
        
        @foreach($dogs as $dog)
            <tr>
                <td>{{ $dog->dog_id }}</td>
                <td>{{ $dog->breed }}</td>
                <td>{{ $dog->sex }}</td>
                <td>{{ $dog->altered }}</td>
                <td>{{ $dog->microchip_id }}</td>
                <td>{{ $dog->surrender_date }}</td>
            </tr>
        @endforeach
    </table>
    
    <a href="{{ url('/reports/animal-control') }}" class="back-link">Back to Report</a>
</body>
</html>

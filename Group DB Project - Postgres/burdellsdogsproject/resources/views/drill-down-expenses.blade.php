<!DOCTYPE html>
<html>
<head>
    <title>Expenses for Dogs Adopted - {{ $month }}</title>
</head>
<style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        padding: 5px;
    }
</style>
<body>
    <h1>Expenses for Dogs Adopted</h1>
    
    <table>
        <tr>
            <th>Dog ID</th>
            <th>Breed</th>
            <th>Sex</th>
            <th>Microchip ID</th>
            <th>Surrender Date</th>
            <th>From Animal Control</th>
            <th>Total Expenses</th>
        </tr>
        
        @foreach($dogs as $dog)
            <tr>
                <td>{{ $dog->dog_id }}</td>
                <td>{{ $dog->breed }}</td>
                <td>{{ $dog->sex }}</td>
                <td>{{ $dog->microchip_id }}</td>
                <td>{{ $dog->surrender_date }}</td>
                <td>{{ $dog->from_animal_control }}</td>
                <td>${{ number_format($dog->total_expenses, 2) }}</td>
            </tr>
        @endforeach
        
        <tr class="total-row">
            <td colspan="6" align="right"><strong>Total:</strong></td>
            <td><strong>${{ number_format($total, 2) }}</strong></td>
        </tr>
    </table>
    
    <a href="{{ url('/reports/animal-control') }}" class="back-link">Back to Report</a>
</body>
</html>
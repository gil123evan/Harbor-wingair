<?php
require_once 'db.php';

$message = "";
$code = $_GET['code'] ?? '';

if (!$code) {
    header("Location: index.php");
    exit;
}

// Handle form submission for update
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $new_desc = trim($_POST['description']);

    if (!empty($new_desc)) {
        try {
            $stmt = $pdo->prepare("UPDATE ticket_type SET description = ? WHERE ticket_type_code = ?");
            $stmt->execute([$new_desc, $code]);
            header("Location: index.php");
            exit;
        } catch (PDOException $e) {
            $message = "Error: " . $e->getMessage();
        }
    } else {
        $message = "Description cannot be empty.";
    }
}

// Fetch current record data
$stmt = $pdo->prepare("SELECT * FROM ticket_type WHERE ticket_type_code = ?");
$stmt->execute([$code]);
$ticket = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$ticket) {
    die("Record not found.");
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit Ticket Type</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f4f7f6; }
        form { background: white; padding: 20px; border-radius: 5px; width: 300px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        input, button { width: 100%; padding: 10px; margin-top: 10px; box-sizing: border-box; }
        button { background: #004080; color: white; border: none; cursor: pointer; }
        button:hover { background: #003366; }
        p { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h2>Edit Ticket Type: <?php echo htmlspecialchars($ticket['ticket_type_code']); ?></h2>
    <?php if($message): ?><p><?php echo htmlspecialchars($message); ?></p><?php endif; ?>
    
    <form method="POST">
        <label>Ticket Type Code (Locked):</label>
        <input type="text" value="<?php echo htmlspecialchars($ticket['ticket_type_code']); ?>" disabled>
        
        <label>Description:</label>
        <input type="text" name="description" value="<?php echo htmlspecialchars($ticket['description']); ?>" required>
        
        <button type="submit">Update Ticket Type</button>
    </form>
    
    <p><a href="index.php">← Back to Dashboard</a></p>
</body>
</html>
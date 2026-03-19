using System.Data.SqlClient;

public class SqliCsharp {
    public void Vulnerable(SqlConnection conn, string userId) {
        var cmd = new SqlCommand();
        cmd.CommandText = $"SELECT * FROM Users WHERE Id = {userId}";
        cmd.CommandText = string.Format("SELECT * FROM Users WHERE Id = {0}", userId);
        cmd.CommandText = "SELECT * FROM Users WHERE Id = " + userId;
        var cmd2 = new SqlCommand($"SELECT * FROM Users WHERE Id = {userId}", conn);
    }
}

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

class FalseNegativeExpansionSqlCSharp {
    void FalseNegativeExpansion(dynamic conn, dynamic context, string userId) {
        var userSql = $"SELECT * FROM Users WHERE Id = {userId}";
        conn.Query<User>(userSql);
        context.Users.FromSqlRaw(userSql);
        context.Database.ExecuteSqlRaw(userSql);
        conn.Execute("UPDATE Users SET Name = '" + userId + "'");
        var cmd = new NpgsqlCommand("SELECT * FROM Users WHERE Id = " + userId, conn);
    }
}

class User { }

class NpgsqlCommand {
    public NpgsqlCommand(string sql, dynamic conn) { }
}

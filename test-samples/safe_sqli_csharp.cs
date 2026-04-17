using System.Data;
using System.Data.SqlClient;

// Safe: Use parameterized queries with SqlCommand
public class SafeSqli
{
    public IDataReader GetUser(SqlConnection conn, string userId)
    {
        using (var cmd = new SqlCommand("SELECT * FROM Users WHERE Id = @id", conn))
        {
            cmd.Parameters.AddWithValue("@id", userId);
            return cmd.ExecuteReader();
        }
    }
}

package prin.udfs;

import io.airlift.slice.Slice;

import io.trino.spi.function.ScalarFunction;
import io.trino.spi.function.Description;
import io.trino.spi.function.SqlType;
import io.trino.spi.function.SqlNullable;
import io.trino.spi.type.StandardTypes;

public class ShowFirstAndLastChar {
    @ScalarFunction(value = "show_first_and_last", deterministic = true)
    @Description("Show only the first and the last characters of a string, the others are hidden by '*'")
    @SqlType(StandardTypes.VARCHAR)
    public static Slice showFirstAndLastChar(
            @SqlNullable @SqlType(StandardTypes.VARCHAR) Slice string) {
        if (string == null)
            return null;

        var strLength = string.length();

        return string;
    }
}
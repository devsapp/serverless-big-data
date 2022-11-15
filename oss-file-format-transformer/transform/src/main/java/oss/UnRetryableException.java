package oss;

public class UnRetryableException extends Exception {

    public static final String OSSExceptionMessageFmt = "RequestID: %s, ErrorCode: %s, ErrorMsg: %s";

    public UnRetryableException() {
    }

    public UnRetryableException(String message) {
        super(message);
    }

    public UnRetryableException(String message, Throwable cause) {
        super(message, cause);
    }

    public UnRetryableException(Throwable cause) {
        super(cause);
    }
}

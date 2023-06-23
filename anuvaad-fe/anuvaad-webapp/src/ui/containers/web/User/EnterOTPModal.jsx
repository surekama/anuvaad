import React, { useEffect, useState } from "react";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import OTPInput from "otp-input-react";
import {
  Button,
  IconButton,
  ThemeProvider,
  Typography,
  withStyles,
} from "@material-ui/core";
import themeAnuvaad from "../../../theme/web/theme-anuvaad";
import CloseIcon from "@material-ui/icons/Close";
import LoginStyles from "../../../styles/web/LoginStyles";

const EnterOTPModal = (props) => {
  const { classes } = props;
  const [OTP, setOTP] = useState("");
  const {
    open,
    handleClose,
    onResend,
    onSubmit,
    OTPModalTitle,
    hideResendOTPButton,
    showTimer,
    // loading,
  } = { ...props };

  const [time, setTime] = useState(120);
  const [running, setRunning] = useState(true);
  useEffect(() => {
    let interval;
    if (showTimer && running) {
      interval = setInterval(() => {
        setTime((prevTime) => {
          if (prevTime > 0) {
            return prevTime - 1;
          } else if (prevTime === 0) {
            clearInterval(interval);
            setTimeout(() => setTime(120), 60000);
            setRunning(false);
            return prevTime;
          }
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [showTimer, running]);

  useEffect(() => {
    const timerId = setTimeout(() => {
      handleClose();
    }, 10 * 60 * 1000);
    return () => clearTimeout(timerId);
  }, []);

  return (
    <ThemeProvider theme={themeAnuvaad}>
      <Dialog
        open={open}
        // onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
        fullWidth
        style={{ backgroundColor: "rgba(255,255,255,0.6)" }}
      >
        <DialogContent
          style={{
            display: "flex",
            justifyContent: "end",
            padding: "5px 0px 0px 0px",
          }}
        >
          {" "}
          <Button
            onClick={() => {
              handleClose();
              setOTP("");
            }}
          >
            <CloseIcon />
          </Button>
        </DialogContent>

        <DialogTitle
          id="alert-dialog-title"
          align="center"
          style={{ paddingTop: "0px" }}
        >
          {OTPModalTitle}
        </DialogTitle>
        <DialogContent
          style={{
            alignSelf: "center",
            margin: !time == 0 ? "28px 50px 28px 50px" : "28px 50px 28px 50px",
            display: "flex",
          }}
        >
          <OTPInput
            value={OTP}
            onChange={setOTP}
            autoFocus
            OTPLength={6}
            otpType="number"
          />
        </DialogContent>
        <DialogContent className={classes.ResendOtpButton}>
          {/* Resend Verification Code ?
            <Button
              style={{
                alignSelf: "center",
                fontFamily: "Roboto, san-serif",
              }}
              // disabled={!time == 0 && showTimer}
              color="primary"
              onClick={() => {
                onResend();
                setOTP("");
                setTime(120);
                setRunning(true);
              }}
            >
              Resend OTP
            </Button> */}
            <div>
            {!time == 0 && showTimer ? (
            <span style={{ paddingLeft: "8px" }}>
              Session expires in -&nbsp;
              {`${Math.floor(time / 60)}`.padStart(2, 0)}:
              {`${time % 60}`.padStart(2, 0)}
            </span>
          ) : (
            <Typography>Your session is expired, Please login again.</Typography>
          )}
            </div>
        </DialogContent>

        <DialogActions
          style={{
            margin: "25px 0px 5px 0px",
            display: "flex",
            justifyContent: "center",
          }}
        >
          <Button
            onClick={() => {
              onResend();
              setOTP("");
              setTime(120);
              setRunning(true);
            }}
            color="primary"
            variant="contained"
            fullWidth
            size="large"
            // disabled={!OTP}
            className={classes.VerifyOtpButton}
          >
            Resend OTP{" "}
          </Button>
          <Button
            onClick={() => onSubmit(OTP)}
            color="primary"
            variant="contained"
            fullWidth
            size="large"
            disabled={!OTP || OTP.length < 6}
            className={classes.VerifyOtpButton}
          >
            VERIFY OTP{" "}
          </Button>
        </DialogActions>
      </Dialog>
    </ThemeProvider>
  );
};

export default withStyles(LoginStyles)(EnterOTPModal);
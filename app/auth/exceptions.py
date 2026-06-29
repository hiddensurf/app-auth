from fastapi import HTTPException,status
credentials_exception_routes=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid username or password",
                            headers={"WWW-Authenticate":"Bearer"},)
credentials_exception_security=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                             detail="Could not validate credentials",
                                             headers={"WWW-Authenticate":"Bearer"}) 
disabled_user_exception=HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                      detail="Inactive user")
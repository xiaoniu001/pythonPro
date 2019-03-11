#include<stdio.h>

char *StrToHex(const char *buf, char *Answer, int LenOfAnswer)
{
    int i = 0;
    if ((int)strlen(buf) % 2 != 0 || (int)strlen(buf) / 2 >= LenOfAnswer)
        return NULL;
    for (i = 0; i < strlen(buf) / 2; i++)
    {
        if (buf[i * 2] >= '0' && buf[i * 2] <= '9')
        {
            Answer[i] = (buf[i * 2] - '0') * 0x10;
            if (buf[i * 2 + 1] >= '0' && buf[i * 2 + 1] <= '9')
                Answer[i] += buf[i * 2 + 1] - '0';
            else if (buf[i * 2 + 1] >= 'A' && buf[i * 2 + 1] <= 'F')
                Answer[i] += buf[i * 2 + 1] - 'A' + 0xA;
            else if (buf[i * 2 + 1] >= 'a' && buf[i * 2 + 1] <= 'f')
                Answer[i] += buf[i * 2 + 1] - 'a' + 0xA;
            else
                break;
        }
        else if (buf[i * 2] >= 'A' && buf[i * 2] <= 'F')
        {
            Answer[i] = (buf[i * 2] - 'A') * 0x10 + 0xA0;
            if (buf[i * 2 + 1] >= '0' && buf[i * 2 + 1] <= '9')
                Answer[i] += buf[i * 2 + 1] - '0';
            else if (buf[i * 2 + 1] >= 'A' && buf[i * 2 + 1] <= 'F')
                Answer[i] += buf[i * 2 + 1] - 'A' + 0xA;
            else if (buf[i * 2 + 1] >= 'a' && buf[i * 2 + 1] <= 'f')
                Answer[i] += buf[i * 2 + 1] - 'a' + 0xA;
            else
                break;
        }
        else if (buf[i * 2] >= 'a' && buf[i * 2] <= 'f')
        {
            Answer[i] = (buf[i * 2] - 'a') * 0x10 + 0xA0;
            if (buf[i * 2 + 1] >= '0' && buf[i * 2 + 1] <= '9')
                Answer[i] += buf[i * 2 + 1] - '0';
            else if (buf[i * 2 + 1] >= 'A' && buf[i * 2 + 1] <= 'F')
                Answer[i] += buf[i * 2 + 1] - 'A' + 0xA;
            else if (buf[i * 2 + 1] >= 'a' && buf[i * 2 + 1] <= 'f')
                Answer[i] += buf[i * 2 + 1] - 'a' + 0xA;
            else
                break;
        }
        else
            break;
        if (i == (strlen(buf) / 2 - 1))
        {
            Answer[LenOfAnswer - 1] = '\0';
            return Answer;
        }
    }
    return NULL;
}


int main()
{
    char hexBuf[5];
    memset(hexBuf, 0, 5);
    printf(StrToHex(buf, hexBuf, 5));

}

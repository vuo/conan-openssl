#include <stdio.h>
#include <openssl/crypto.h>

int main()
{
	printf("Successfully initialized OpenSSL %s\n", SSLeay_version(SSLEAY_VERSION));
	return 0;
}

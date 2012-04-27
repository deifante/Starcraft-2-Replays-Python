#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

unsigned int cryptTable[0x500];
void InitialiseCryptTable();
void DecryptData(void * buffer, unsigned int length, unsigned int key);
unsigned int HashString(unsigned char *str, unsigned int hashType);

int main()
{
  int i = 0;
  unsigned int hashValue = 0;
  char * str = 0;
  int length = 0;
  int encryptedBlockData[4];
  encryptedBlockData[0] = 824787133;
  encryptedBlockData[1] = 2393494642;
  encryptedBlockData[2] = 2479920305;
  encryptedBlockData[3] = 3368241304;

  /* str = calloc(26, 1); */
  InitialiseCryptTable();
  /* strcpy(str, "arr\\units.dat"); */

  /* for(i=0; i<4; ++i) */
  /*   printf("hashValue{%d} of '%s' = 0x%X\n", i, str, HashString(str, i)); */
  
  /* strcpy(str, "unit\\neutral\\acritter.grp"); */
  /* for(i=0; i<4; ++i) */
  /*   printf("hashValue{%d} of '%s' = 0x%X\n", i, str, HashString(str, i)); */

  /* strcpy(str, "1234567"); */
  /* length = (int)strlen(str); */
  /* printf("Decrypted Data (%s): ", str); */
  /* DecryptData((void*)str, (unsigned int)strlen(str), 14); */
  /* for(i=0; i<length; ++i) */
  /*     printf("%d ", (int)str[i]); */

  /* free(str); */

  hashValue = HashStringBlue("(block table)", 3);
  printf("Decrypt Key: %X\n", hashValue);

  printf("Before\n\t");
  for(i=0; i<4; ++i)
      printf("%u ", encryptedBlockData[i]);
  puts("");
  DecryptData((void*)encryptedBlockData, (unsigned int)(sizeof(int)*4), hashValue);
  printf("After\n\t");
  for(i=0; i<4; ++i)
      printf("%u ", encryptedBlockData[i]);
  printf("Done\n");
}

void InitialiseCryptTable()
{
 unsigned int seed   = 0x00100001;
 unsigned int index1 = 0;
 unsigned int index2 = 0;
 unsigned int temp1  = 0;
 unsigned int temp2  = 0;
 int i = 0;

 for(index1 = 0; index1 < 0x100; index1++)
   {
      for (index2 = index1, i = 0; i < 5; i++, index2 += 0x100)
        {
          seed = (seed * 125 + 3) % 0x2AAAAB;
          temp1 = (seed & 0xFFFF) << 0x10;

          seed = (seed * 125 + 3) % 0x2AAAAB;
          temp2 = (seed & 0xFFFF);
          cryptTable[index2] = (temp1 | temp2);
        }
    }
}

void DecryptData(void * buffer, unsigned int length, unsigned int key)
{
  unsigned int * intBuffer = (unsigned int *)buffer;
  unsigned int seed = 0xEEEEEEEE;
  unsigned int ch   = 0;

  // If the data isn't a multiple of ints then the remaining bytes
  // will not get decrypted.
  length >>= 2;
  printf("start value of length %d\n", length);
  while (length-- > 0)
    {
      seed += cryptTable[0x400 + (key & 0xFF)];
      printf("loop (length %d)\n", length);
      ch = *intBuffer ^ (key + seed);
      key = ((~key << 0x15) + 0x11111111) | (key >> 0x0B);
      seed = ch + seed + (seed << 5) + 3;
      printf("ch: %u\n", ch);
      *intBuffer++ = ch;
    }
}

unsigned int HashString(unsigned char *str, unsigned int hashType)
{
  unsigned int seed1 = 0x7FED7FED;
  unsigned int seed2 = 0xEEEEEEEE;
  int ch = 0;

  while (*str != 0)
    {
      ch = toupper(*str++);
      seed1 = cryptTable[(hashType << 8) + ch] ^ (seed1 + seed2);
      seed2 = ch + seed1 + seed2 + (seed2 << 5 ) + 3;
    }
  return seed1;
}

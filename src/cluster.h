/* Declare everything, Fortran & C -- so we can register them */
#include <Python.h>

#ifdef ENABLE_NLS
#include <libintl.h>

#define _(String) dgettext ("cluster", String)
#else
#define _(String) (String)
#endif

// These codes must match those in ../R/clara.q  <==>  'diss_kind'
typedef enum {
    EUCLIDEAN = 1,
    MANHATTAN = 2,
    JACCARD = 3
} DISS_KIND;

/* --------- ./clara.c ------------------*/

double randm(int *nrun);

void cl_clara(int *n,  /* = number of objects */
              int *jpp,/* = number of variables */
              int *kk, /* = number of clusters, 1 <= kk <= n-1 */
              double *x,	/* Input:  the data x[n, jpp] _rowwise_ (transposed)
				 * Output: the first `n' values are the `clustering'
				 *	   (integers in 1,2,..,kk) */
              int *nran,	/* = #{random samples} drawn	   (= `samples' in R)*/
              int *nsam,	/* = #{objects} drawn from data set (`sampsize' in R) */
              double *dys,/* [1:(1 + (nsam * (nsam - 1))/2)]
			   * Output: to contain the distances */
              int *mdata,	/*= {0,1}; 1: min(x) is missing value (NA);  0: no NA */
              double *valmd,/*[j]= missing value code (instead of NA) for x[,j]*/
              int *jtmd,	/* [j]= {-1,1};	 -1: x[,j] has NA; 1: no NAs in x[,j] */
              int *diss_kind, // = {EUCLIDEAN, MANHATTAN, JACCARD}
              int/*logical*/ *py_rng,/*= {0,1};  0 : use clara's internal weak RNG;
				     *	        1 : use common RNG with Python */
              int/*logical*/ *pam_like,/* if (1), we do "swap()" as in pam(), otherwise
					  use the code as it was in clara() "forever"
					  upto 2011-04 */
              int *correct_d,/* option for dist.computation: if (0), use the "fishy"
			     formula to update distances in the NA-case,
			     if (1), use a dysta2()-compatible formula */
              int *nrepr, /* logical (0/1): 1 = "is representative object"  */
              int *nsel,
              int *nbest,/* x[nbest[j],] : the j-th obs in the final sample */
              int *nr, int *nrx,/* prov. and final "medoids" aka representatives */
              double *radus, double *ttd, double *ratt,
              double *ttbes, double *rdbes, double *rabes,
              int *mtt, double *obj,
              double *avsyl, double *ttsyl, double *sylinf,
              int *jstop, int *trace_lev,
              double *tmp, /* = double [ 3 * nsam ] */
              int *itmp	/* = integer[ 6 * nsam ] */
              );


void dysta2(int nsam, int jpp, int *nsel,
	    double *x, int n, double *dys, int diss_kind,
	    int *jtmd, double *valmd, int has_NA, int *toomany_NA);


void bswap2(int kk, int nsam, double s, const double dys[],
	    int pam_like, int trace_lev,
	    // result:
	    double *sky, int *nrepr,
	    double *dysma, double *dysmb, double *beter);

void selec(int kk, int n, int jpp, int diss_kind,
	   double *zb, int nsam, int has_NA, int *jtmd, double *valmd,
	   int trace_lev,
	   int *nrepr, int *nsel, double *dys, double *x, int *nr,
	   int *nafs, double *ttd, double *radus, double *ratt,
	   int *nrnew, int *nsnew, int *npnew, int *ns, int *np, int *new,
	   double *ttnew, double *rdnew, int correct_d);

void resul(int kk, int n, int jpp, int diss_kind, int has_NA,
	   int *jtmd, double *valmd, double *x, int *nrx, int *mtt, int correct_d);

void black(int kk, int jpp, int nsam, int *nbest,
	   double *dys, double s, double *x,
	   /* --> Output : */
	   double *avsyl, double *ttsyl, double *sylinf,
	   int *ncluv, int *nsend, int *nelem, int *negbr,
	   double *syl, double *srank);


#ifndef VQETASKS_DIAGONALIZETASK_HPP_
#define VQETASKS_DIAGONALIZETASK_HPP_

#include "VQETask.hpp"
#include "PauliOperator.hpp"

namespace xacc {
namespace vqe {

class DiagonalizeTask : public VQETask {

public:

	DiagonalizeTask() {}

	DiagonalizeTask(std::shared_ptr<VQEProgram> prog) :
			VQETask(prog) {
	}

	virtual VQETaskResult execute(Eigen::VectorXd parameters);

	/**
	 * Return the name of this instance.
	 *
	 * @return name The string name
	 */
	virtual const std::string name() const {
		return "vqe-diagonalize";
	}

	/**
	 * Return the description of this instance
	 * @return description The description of this object.
	 */
	virtual const std::string description() const {
		return "Diagonalize the Qubit Hamiltonian "
				"and return the lowest energy eigenvalue.";
	}

	/**
	 * Return an empty options_description, this is for
	 * subclasses to implement.
	 */
	virtual OptionPairs getOptions() {
		OptionPairs desc{{"diagonalize-backend",
							"The backend to use to compute the Hamiltonian eigenspectrum"},{
			"diag-number-symmetry","Reduce the dimensionality of the problem by considering Hamiltonian subspace spanned by NELEC occupations."},{
            "print-ground-state","Also print the eigenvector corresponding to the min eigenvalue"}};
		return desc;
	}

};

class DiagonalizeBackend : public Identifiable {
public:
	virtual double diagonalize(PauliOperator& prog) = 0;
	virtual double diagonalize(std::shared_ptr<VQEProgram> prog) = 0;
    virtual std::pair<double, Eigen::VectorXcd> diagonalizeWithGroundState(std::shared_ptr<VQEProgram> prog) {
        return {diagonalize(prog),Eigen::VectorXcd::Zero(1)};
    }
	virtual ~DiagonalizeBackend() {}
};

class EigenDiagonalizeBackend: public DiagonalizeBackend {
protected:
    Eigen::SelfAdjointEigenSolver<Eigen::MatrixXcd> es;
public:

	double diagonalize(PauliOperator& prog) override;
	double diagonalize(std::shared_ptr<VQEProgram> prog) override;
    std::pair<double, Eigen::VectorXcd> diagonalizeWithGroundState(std::shared_ptr<VQEProgram> prog) override;
	const std::string name() const override {
		return "diagonalize-eigen";
	}

	/**
	 * Return the description of this instance
	 * @return description The description of this object.
	 */
	const std::string description() const override {
		return "";
	}
};

}
}
#endif
